from typing import Any, Dict, List, Type, Union, Callable, Optional, get_args, get_origin, get_type_hints

from .._models import BaseModel

__all__ = [
    "Tool",
    "Function",
    "ToolCall",
    "ToolChoice",
    "FunctionTool",
    "function_tool",
]


class FunctionTool(BaseModel):
    type: str = "function"
    function: "Function"


class Function(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]


class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: "FunctionCall"


class FunctionCall(BaseModel):
    name: str
    arguments: str


class ToolChoice(BaseModel):
    type: str = "function"
    function: "ToolChoiceFunction"


class ToolChoiceFunction(BaseModel):
    name: str


Tool = Union[FunctionTool, Dict[str, Any]]


def _get_json_type(py_type: Type[Any]) -> str:
    """Map Python types to JSON schema types."""
    py_type = get_origin(py_type) or py_type

    if py_type is int or py_type is float:
        return "number"
    if py_type is str:
        return "string"
    if py_type is bool:
        return "boolean"
    if py_type is list:
        return "array"
    if py_type is dict or py_type is object:
        return "object"
    return "string"


def _python_type_to_json_schema(py_type: Any, description: str = "") -> Dict[str, Any]:
    """Convert a Python type to JSON schema."""
    origin = get_origin(py_type)

    if origin is Union:
        args = get_args(py_type)
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            result = _python_type_to_json_schema(non_none[0], description)
            if type(None) in args:
                result["nullable"] = True
            return result

    if origin is list:
        args = get_args(py_type)
        if args:
            return {
                "type": "array",
                "items": _python_type_to_json_schema(args[0]),
            }
        return {"type": "array", "items": {}}

    if origin is dict:
        args = get_args(py_type)
        if len(args) == 2:
            return {
                "type": "object",
                "additionalProperties": _python_type_to_json_schema(args[1]),
            }
        return {"type": "object"}

    json_type = _get_json_type(py_type)
    result = {"type": json_type}
    if description:
        result["description"] = description
    return result


def _extract_parameters(func: Callable[..., Any]) -> Dict[str, Any]:
    """Extract JSON schema parameters from a Python function's type hints."""
    try:
        hints = get_type_hints(func)
    except Exception:
        hints = {}

    properties: Dict[str, Any] = {}
    required: List[str] = []

    for param_name, param_type in hints.items():
        if param_name in ("return", "self", "cls"):
            continue

        import inspect

        sig = inspect.signature(func)
        param = sig.parameters.get(param_name)
        param_description = ""
        if param and param.default is not inspect.Parameter.empty:
            param_description = f"Default: {param.default}"

        properties[param_name] = _python_type_to_json_schema(param_type, param_description)

        if param is None or param.default is inspect.Parameter.empty:
            required.append(param_name)

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }


def function_tool(
    func: Callable[..., Any],
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a tool definition from a Python function.

    Args:
        func: The Python function to convert to a tool
        name: Optional name for the tool (defaults to function name)
        description: Optional description (defaults to function docstring)

    Returns:
        A dictionary representing the tool that can be passed to the API
    """
    tool_name = name or func.__name__
    tool_description = description or func.__doc__ or ""

    parameters = _extract_parameters(func)

    return {
        "type": "function",
        "function": {
            "name": tool_name,
            "description": tool_description.strip(),
            "parameters": parameters,
        },
    }
