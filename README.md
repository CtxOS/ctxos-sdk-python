# Ctxos Python API Library

[![PyPI version](https://img.shields.io/pypi/v/ctxos.svg)](https://pypi.org/project/ctxos/)

The Ctxos Python library provides convenient access to the Ctxos REST API from any Python 3.7+
application. It includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Migration from v0.2.x and below

In `v0.3.0`, we introduced a fully rewritten SDK.

The new version uses separate sync and async clients, unified streaming, typed params and structured response objects, and resource-oriented methods:

**Sync before/after:**

```diff
- client = ctxos.Client(os.environ["CTXOS_API_KEY"])
+ client = ctxos.Ctxos(api_key=os.environ["CTXOS_API_KEY"])
  # or, simply provide an CTXOS_API_KEY environment variable:
+ client = ctxos.Ctxos()

- rsp = client.completion(**params)
- rsp["completion"]
+ rsp = client.completions.create(**params)
+ rsp.completion
```

**Async before/after:**

```diff
- client = ctxos.Client(os.environ["CTXOS_API_KEY"])
+ client = ctxos.AsyncCtxos(api_key=os.environ["CTXOS_API_KEY"])

- await client.acompletion(**params)
+ await client.completions.create(**params)
```

The `.completion_stream()` and `.acompletion_stream()` methods have been removed;
simply pass `stream=True`to `.completions.create()`.

<details>
<summary>Example streaming diff</summary>

```diff py
  import ctxos

- client = ctxos.Client(os.environ["CTXOS_API_KEY"])
+ client = ctxos.Ctxos()

  # Streams are now incremental diffs of text
  # rather than sending the whole message every time:
  text = "
- stream = client.completion_stream(**params)
- for data in stream:
-     diff = data["completion"].replace(text, "")
-     text = data["completion"]
+ stream = client.completions.create(**params, stream=True)
+ for data in stream:
+     diff = data.completion # incremental text
+     text += data.completion
      print(diff, end="")

  print("Done. Final text is:")
  print(text)
```

</details>

## Installation

```sh
pip install ctxos
```

## Usage

```python
from ctxos import Ctxos

client = Ctxos(
    # defaults to os.environ.get("CTXOS_API_KEY")
    api_key="my api key",
)

completion = client.complete.create(
    model="ctxos-1",
    prompt="how does a court case get to the Supreme Court?",
)
print(completion.choices[0].text)
```

While you can provide an `api_key` keyword argument, we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
and adding `CTXOS_API_KEY="my api key"` to your `.env` file so that your API Key is not stored in source control.

## Async Usage

Simply import `AsyncCtxos` instead of `Ctxos` and use `await` with each API call:

```python
from ctxos import AsyncCtxos

client = AsyncCtxos(
    # defaults to os.environ.get("CTXOS_API_KEY")
    api_key="my api key",
)


async def main():
    completion = await client.complete.create(
        model="ctxos-1",
        prompt="how does a court case get to the Supreme Court?",
    )
    print(completion.choices[0].text)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.

## Streaming Responses

We provide support for streaming responses using Server Side Events (SSE).

```python
from ctxos import Ctxos

client = Ctxos()

stream = client.complete.create(
    prompt="Your prompt here",
    model="ctxos-1",
    stream=True,
)
for completion in stream:
    print(completion.choices[0].text)
```

The async client uses the exact same interface.

```python
from ctxos import AsyncCtxos

client = AsyncCtxos()

stream = await client.complete.create(
    prompt="Your prompt here",
    model="ctxos-1",
    stream=True,
)
async for completion in stream:
    print(completion.choices[0].text)
```

The async client uses the exact same interface.

```python
from ctxos import AsyncCtxos

ctxos = AsyncCtxos()

stream = await ctxos.completions.create(
    prompt=f"{HUMAN_PROMPT} Your prompt here {AI_PROMPT}",
    max_tokens_to_sample=300,
    model="ctxos-1",
    stream=True,
)
async for completion in stream:
    print(completion.completion)
```

## Tools / Function Calling

The SDK supports tools (also known as function calling), allowing the model to call your Python functions and return structured data.

### Defining Tools

Use the `function_tool` helper to convert Python functions into tool definitions:

```python
from ctxos import Ctxos
from ctxos.types import function_tool

def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the weather for a location."""
    return f"Weather in {location}: 72 degrees {unit}"

def get_stock_price(symbol: str) -> float:
    """Get the current stock price for a symbol."""
    return 150.25

client = Ctxos()

# Create tool definitions
tools = [
    function_tool(get_weather),
    function_tool(get_stock_price),
]
```

### Calling with Tools

```python
response = client.completions.create(
    model="ctxos-1",
    prompt="What's the weather in San Francisco and what's AAPL's stock price?",
    tools=tools,
)

# Process tool calls from the response
for choice in response.choices or []:
    if choice.tool_calls:
        for tool_call in choice.tool_calls:
            print(f"Called: {tool_call.function.name}")
            print(f"Arguments: {tool_call.function.arguments}")
```

### Tool Choice

Control which tool the model calls using `tool_choice`:

```python
# Allow the model to decide (default)
response = client.completions.create(
    model="ctxos-1",
    prompt="What's the weather?",
    tools=tools,
    tool_choice="auto",
)

# Force a specific tool
response = client.completions.create(
    model="ctxos-1",
    prompt="What's the weather?",
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_weather"}},
)

# Disable tool calling
response = client.completions.create(
    model="ctxos-1",
    prompt="Hello!",
    tools=tools,
    tool_choice="none",
)
```

### Manual Tool Definition

You can also define tools manually using dictionaries:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    }
]
```

## Using Types

Nested request parameters are [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict), while responses are [Pydantic](https://pydantic-docs.helpmanual.io/) models. This helps provide autocomplete and documentation within your editor.

If you would like to see type errors in VS Code to help catch bugs earlier, set `python.analysis.typeCheckingMode` to `"basic"`.

## Handling errors

When the library is unable to connect to the API (e.g., due to network connection problems or a timeout), a subclass of `ctxos.APIConnectionError` is raised.

When the API returns a non-success status code (i.e., 4xx or 5xx
response), a subclass of `ctxos.APIStatusError` will be raised, containing `status_code` and `response` properties.

All errors inherit from `ctxos.APIError`.

```python
from ctxos import Ctxos

client = Ctxos()

try:
    client.complete.create(
        prompt="Your prompt here",
        model="ctxos-1",
    )
except ctxos.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except ctxos.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except ctxos.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

### Retries

Certain errors will be automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 409 Conflict, 429 Rate Limit,
and >=500 Internal errors will all be retried by default.

You can use the `max_retries` option to configure or disable this:

```python
from ctxos import Ctxos

# Configure the default for all requests:
client = Ctxos(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
client.with_options(max_retries=5).complete.create(
    prompt="Can you help me effectively ask for a raise at work?",
    model="ctxos-1",
)
```

### Timeouts

Requests time out after 60 seconds by default. You can configure this with a `timeout` option,
which accepts a float or an [`httpx.Timeout`](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration):

```python
import httpx
from ctxos import Ctxos

# Configure the default for all requests:
client = Ctxos(
    # default is 60s
    timeout=20.0,
)

# More granular control:
client = Ctxos(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5 * 1000).complete.create(
    prompt="Where can I get a good coffee in my neighbourhood?",
    model="ctxos-1",
)
```

On timeout, an `APITimeoutError` is thrown.

Note that requests which time out will be [retried twice by default](#retries).

## Default Headers

If you need to, you can override it by setting default headers per-request or on the client object.

Be aware that doing so may result in incorrect types and other unexpected or undefined behavior in the SDK.

```python
from ctxos import Ctxos

ctxos = Ctxos(
    default_headers={"ctxos-version": "My-Custom-Value"},
)
```

## Advanced: Configuring custom URLs, proxies, and transports

You can configure the following keyword arguments when instantiating the client:

```python
import httpx
from ctxos import Ctxos

ctxos = Ctxos(
    # Use a custom base URL
    base_url="http://my.test.server.example.com:8083",
    proxies="http://my.test.proxy.example.com",
    transport=httpx.HTTPTransport(local_address="0.0.0.0"),
)
```

See the httpx documentation for information about the [`proxies`](https://www.python-httpx.org/advanced/#http-proxying) and [`transport`](https://www.python-httpx.org/advanced/#custom-transports) keyword arguments.

## Status

This package is in beta. Its internals and interfaces are not stable and subject to change without a major semver bump;
please reach out if you rely on any undocumented behavior.

We are keen for your feedback; please open an [issue](https://www.github.com/ctxos/ctxos-sdk-python/issues) with questions, bugs, or suggestions.

## Requirements

Python 3.9 or higher.
