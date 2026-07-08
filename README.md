# GenLayer Documentation MCP Server

A standardized, shareable Model Context Protocol (MCP) server that packages and exposes the GenLayer documentation (`genlayer-docs (3).txt`) to any AI assistant (including Claude Desktop, Cursor, Windsurf, Gemini, and others).

By packaging this as a Python project with a `pyproject.toml` and utilizing the official `mcp` SDK, anyone can run it instantly with zero manual file path or dependency setup.

## Available Tools

Once registered, the server exposes the following tools:

1. **`search_docs(query: string, top_k: int = 5)`**:
   Search the GenLayer documentation for relevant sections matching a query. Returns top matching sections along with their hierarchical title breadcrumbs (e.g., `What is GenLayer > Core Technology > On-Chain AI Processing`) and starting line numbers.
   
2. **`get_section(title: string)`**:
   Retrieve the full content of a specific documentation section matching the specified heading title.

3. **`list_sections()`**:
   List all headings and subheadings present in the GenLayer documentation along with their starting line numbers.

---

## Universal Running & Setup Options

You can run this server using standard Python tools. We recommend using **`uv`** (a fast Python package manager) for a zero-install experience, or standard **`pip`/`pipx`**.

### Option A: Running Locally (For Development)

If you have cloned or downloaded this directory locally to `c:\Users\MueAb\Desktop\Genlayer mcp`:

#### 1. Claude Desktop Setup
Open your Claude configuration file (on Windows: `%APPDATA%\Claude\claude_desktop_config.json`) and add the server inside the `mcpServers` block:

* **Using `uvx` (Easiest, zero-install)**:
  ```json
  {
    "mcpServers": {
      "genlayer-docs": {
        "command": "uvx",
        "args": [
          "--from",
          "c:\\Users\\MueAb\\Desktop\\Genlayer mcp",
          "genlayer-docs-mcp"
        ]
      }
    }
  }
  ```

* **Using installed python package**:
  If you have installed the package via `pip install -e .` (or `pip install .`):
  ```json
  {
    "mcpServers": {
      "genlayer-docs": {
        "command": "python",
        "args": [
          "-m",
          "genlayer_docs_mcp.server"
        ]
      }
    }
  }
  ```

#### 2. Cursor IDE / Windsurf Setup
Register the server in your editor's MCP settings:
* **Type**: `command`
* **Command**: `uvx --from "c:\Users\MueAb\Desktop\Genlayer mcp" genlayer-docs-mcp`

---

### Option B: Publishing & Distributing to PyPI (For Everyone)

If you publish this package to PyPI (e.g., under the name `genlayer-docs-mcp`), **anyone in the world** can use it on **any AI client** instantly with zero local files!

#### 1. Claude Desktop Setup
Any user can simply add this to their `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "genlayer-docs": {
      "command": "uvx",
      "args": ["genlayer-docs-mcp"]
    }
  }
}
```

#### 2. Cursor IDE / Windsurf Setup
* **Type**: `command`
* **Command**: `uvx genlayer-docs-mcp`

---

### Option C: Installation via `pipx` or `pip`
Users who prefer not to use `uvx` can install the server globally using `pipx`:

```bash
# Install globally from PyPI
pipx install genlayer-docs-mcp

# Or install globally from local directory
pipx install c:\Users\MueAb\Desktop\Genlayer mcp
```

Then configure the command in any AI client as:
* **Command**: `genlayer-docs-mcp` (no arguments required)
