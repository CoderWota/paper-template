"""Call the installed official MCP servers from record-preserving workspace scripts.

The parent uses only the standard library. The worker uses the isolated MCP runtime.
Credentials are loaded inside the worker, never passed in command arguments or JSON.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


class MCPError(RuntimeError):
    pass


def call_tool(root: Path, server: str, tool: str, arguments: dict, timeout: float = 120) -> dict:
    interpreter = root / ".tools/mcp/python" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not interpreter.is_file():
        raise MCPError("MCP runtime is missing. Run scripts/setup_mcp.py install and configure.")
    try:
        result = subprocess.run([str(interpreter), str(root / "scripts/mcp_bridge.py"), "--worker"],
                                input=json.dumps({"server": server, "tool": tool, "arguments": arguments, "timeout": timeout}),
                                capture_output=True, text=True, encoding="utf-8", timeout=timeout + 20, cwd=root)
        payload = json.loads(result.stdout)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        raise MCPError("MCP call did not return a usable response; do not automatically repeat an upload.") from None
    if result.returncode or payload.get("error"):
        raise MCPError(payload.get("error") or "MCP worker failed.")
    if payload.get("isError", payload.get("is_error", False)):
        raise MCPError("The MCP tool reported a service error; no direct API fallback was attempted.")
    return payload


def tool_data(result: dict):
    structured = result.get("structuredContent", result.get("structured_content"))
    if structured is not None:
        return structured
    for block in result.get("content", []):
        if block.get("type") == "text":
            try:
                return json.loads(block["text"])
            except ValueError:
                return {"text": block["text"]}
    raise MCPError("MCP returned no structured data or text.")


async def worker(request: dict) -> dict:
    import asyncio
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from setup_mcp import ROOT, launch_command, server_env

    server = request["server"]
    if server not in ("sciverse", "mineru"):
        return {"error": "Only the configured official Sciverse and MinerU MCP servers are supported."}
    command = launch_command(ROOT, server)
    params = StdioServerParameters(command=command[0], args=command[1:], cwd=str(ROOT / ".tools/mcp"),
                                  env=server_env(ROOT, server))
    async with asyncio.timeout(request["timeout"]):
        with open(os.devnull, "w") as quiet:
            async with stdio_client(params, errlog=quiet) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    listing = await session.list_tools()
                    tool = next((t for t in listing.tools if t.name == request["tool"]), None)
                    # Refusals are returned, not raised: an exception inside the session task group arrives wrapped.
                    if tool is None:
                        return {"error": "The requested operation is not exposed by the installed MCP server."}
                    arguments = request["arguments"]
                    schema = tool.model_dump(by_alias=True, exclude_none=True).get("inputSchema", {})
                    if set(arguments) - set(schema.get("properties", {})) or set(schema.get("required", [])) - set(arguments):
                        return {"error": "The requested parameters are not supported by the installed MCP tool."}
                    result = await session.call_tool(tool.name, arguments=arguments, read_timeout_seconds=request["timeout"])
                    return result.model_dump(by_alias=True, exclude_none=True)


def main() -> int:
    import asyncio
    from setup_mcp import SetupError
    try:
        request = json.load(sys.stdin)
        result = asyncio.run(worker(request))
    except SetupError as error:
        result = {"error": str(error)}
    except Exception:
        # Upstream exceptions may contain signed transfer URLs or request headers, so only a fixed message is printed.
        result = {"error": "MCP operation failed. Check the MCP setup with scripts/setup_mcp.py check; do not bypass it with a direct API or CLI."}
    print(json.dumps(result, ensure_ascii=False))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    raise SystemExit(main())
