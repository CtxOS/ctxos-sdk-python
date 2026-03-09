import json
from typing import Any, Dict, List, Optional

__all__ = ["BaseTool", "ToolUser"]


class BaseTool:
    """
    Base class for defining tools that can be used with ctxos.

    To create a tool, inherit from this class and implement the use_tool() method.

    Example:
        class GetWeatherTool(BaseTool):
            def use_tool(self, location: str, unit: str = "celsius") -> str:
                return f"Weather in {location}: 72 degrees {unit}"

        tool = GetWeatherTool(
            name="get_weather",
            description="Get the weather for a location",
            parameters=[
                {"name": "location", "type": "str", "description": "City name"},
                {"name": "unit", "type": "str", "description": "Temperature unit"},
            ]
        )
    """

    def __init__(
        self,
        name: str,
        description: str,
        parameters: List[Dict[str, str]],
    ):
        self.name = name
        self.description = description
        self.parameters = parameters

    def use_tool(self, **kwargs: Any) -> Any:
        """
        Implement this method to define what your tool does.

        Args:
            **kwargs: The arguments passed to the tool

        Returns:
            Any: The result of the tool execution
        """
        raise NotImplementedError("Subclasses must implement use_tool()")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary for the API."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        param["name"]: {
                            "type": param["type"],
                            "description": param.get("description", ""),
                        }
                        for param in self.parameters
                    },
                    "required": [param["name"] for param in self.parameters if param.get("required", False)],
                },
            },
        }


class ToolUser:
    """
    ToolUser allows you to use ctxos with a list of tools.

    Example:
        tool = GetWeatherTool(...)
        tool_user = ToolUser([tool])

        # Manual mode - returns tool arguments for you to execute
        messages = [{"role": "user", "content": "What's the weather in LA?"}]
        result = tool_user.use_tools(messages, execution_mode="manual")

        # Automatic mode - executes the tool automatically
        messages = [{"role": "user", "content": "What's the weather in LA?"}]
        result = tool_user.use_tools(messages, execution_mode="automatic")
    """

    def __init__(self, tools: List[BaseTool]):
        self.tools = tools

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return next((t for t in self.tools if t.name == name), None)

    def use_tools(
        self,
        messages: List[Dict[str, Any]],
        execution_mode: str = "manual",
    ) -> List[Dict[str, Any]]:
        """
        Use tools with the given messages.

        Args:
            messages: List of message dicts with keys: role, content, tool_inputs, tool_outputs, tool_error
            execution_mode: "automatic" to execute tools, "manual" to return arguments

        Returns:
            Updated messages list including tool_inputs/tool_outputs
        """
        from .. import Ctxos

        client = Ctxos()
        tool_definitions = [tool.to_dict() for tool in self.tools]  # type: ignore[list-item]

        response = client.complete.create(
            model="ctxos-1",
            prompt=messages[-1]["content"],
            tools=tool_definitions,  # type: ignore[arg-type]
        )

        choices = response.choices
        if not choices:
            return messages

        choice = choices[0]
        if not choice:
            return messages

        tool_calls = choice.tool_calls

        if not tool_calls:
            messages.append(
                {
                    "role": "assistant",
                    "content": choice.text or "",
                }
            )
            return messages

        tool_inputs_message: Dict[str, Any] = {
            "role": "tool_inputs",
            "content": "",
            "tool_inputs": [
                {
                    "tool_name": tc.function.name,
                    "tool_arguments": tc.function.arguments,
                }
                for tc in tool_calls
            ],
        }

        if execution_mode == "automatic":
            tool_outputs: List[Dict[str, Any]] = []
            for tool_call in tool_calls:
                tool = self.get_tool(tool_call.function.name)
                if tool is None:
                    tool_outputs.append(
                        {
                            "tool_name": tool_call.function.name,
                            "output": None,
                            "error": f"No tool named {tool_call.function.name} available.",
                        }
                    )
                    continue

                try:
                    args = json.loads(tool_call.function.arguments)
                    result = tool.use_tool(**args)
                    tool_outputs.append(
                        {
                            "tool_name": tool_call.function.name,
                            "output": str(result),
                        }
                    )
                except Exception as e:
                    tool_outputs.append(
                        {
                            "tool_name": tool_call.function.name,
                            "output": None,
                            "error": str(e),
                        }
                    )

            messages.append(tool_inputs_message)
            messages.append(
                {
                    "role": "tool_outputs",
                    "content": "",
                    "tool_outputs": tool_outputs,
                    "tool_error": None,
                }
            )

            second_response = client.complete.create(
                model="ctxos-1",
                prompt="Continue the conversation given the tool results.",
                tools=tool_definitions,  # type: ignore[arg-type]
            )

            second_choices = second_response.choices
            second_text = second_choices[0].text if second_choices and second_choices[0].text else ""
            messages.append(
                {
                    "role": "assistant",
                    "content": second_text,
                }
            )
        else:
            messages.append(tool_inputs_message)

        return messages
