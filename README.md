# GenLayer Documentation MCP Server

A standardized, shareable Model Context Protocol (MCP) server that packages and exposes the GenLayer documentation (`genlayer-docs.txt`) to any AI assistant (including Claude Desktop, Cursor, Windsurf, Gemini, and others).

By packaging this as a Python project with a `pyproject.toml` and utilizing the official `mcp` SDK, anyone can run it with a standard Python install — no manual file paths or dependency wrangling.

## Available Tools

Once registered, the server exposes the following tools:

1. **`search_docs(query: string, top_k: int = 5)`**:
   Search the GenLayer documentation for relevant sections matching a query. Returns top matching sections along with their hierarchical title breadcrumbs (e.g., `What is GenLayer > Core Technology > On-Chain AI Processing`) and starting line numbers.

2. **`get_section(title: string)`**:
   Retrieve the full content of a specific documentation section matching the specified heading title.

3. **`list_sections()`**:
   List all headings and subheadings present in the GenLayer documentation along with their starting line numbers.

---

## Quick Start (Recommended)

This is the setup verified to work with a standard Python installation on Windows, macOS, and Linux.

### 1. Install the package

From PyPI:

```bash
pip install genlayer-docs-mcp
```

Or from source (after cloning this repo):

```bash
pip install .
```

### 2. Register it with your AI client

Add the server inside the `mcpServers` block of your client's MCP config
(Claude Desktop on Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "genlayer-docs": {
      "command": "python",
      "args": [
        "-m",
        "genlayer_docs_mcp"
      ]
    }
  }
}
```

> **Why `python -m`?** It uses the Python interpreter already on your `PATH`, so
> there is nothing extra to install (unlike `uvx`, which requires `uv` to be
> installed first). Restart your client after saving, and the three tools above
> will appear.

For **Cursor / Windsurf**, use the same values in the editor's MCP settings:
* **Type**: `command`
* **Command**: `python`
* **Args**: `-m genlayer_docs_mcp`

---

## Alternative: Zero-install with `uvx`

If you have [`uv`](https://docs.astral.sh/uv/) installed, you can run the server
without installing it first. Anyone in the world can use this on any AI client
with zero local files:

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

Cursor / Windsurf command: `uvx genlayer-docs-mcp`

> Requires `uv`/`uvx` on your `PATH`. Install it with `winget install astral-sh.uv`
> (Windows) or see the [uv install guide](https://docs.astral.sh/uv/getting-started/installation/).

---

## Alternative: Install directly from GitHub (no PyPI needed)

To track the latest source, install straight from the public repository:

* **Using `pip`**:
  ```bash
  pip install "git+https://github.com/Laegend14/Genlayer-mcp"
  ```

* **Using `uvx` (zero-install)**:
  ```json
  {
    "mcpServers": {
      "genlayer-docs": {
        "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/Laegend14/Genlayer-mcp",
          "genlayer-docs-mcp"
        ]
      }
    }
  }
  ```

---

## Alternative: Global install via `pipx`

Users who prefer an isolated global install can use `pipx`:

```bash
# From PyPI
pipx install genlayer-docs-mcp

# Or from GitHub
pipx install "git+https://github.com/Laegend14/Genlayer-mcp"
```

Then configure the command in any AI client as:
* **Command**: `genlayer-docs-mcp` (no arguments required)

> Note: this requires the `pipx` scripts directory to be on your `PATH`
> (`pipx ensurepath`). If your client can't find the `genlayer-docs-mcp`
> executable, use the **Quick Start** `python -m` method instead.

---

## Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/Laegend14/Genlayer-mcp
cd Genlayer-mcp
pip install -e .
```

Run the server directly to confirm it loads the documentation:

```bash
python -m genlayer_docs_mcp
```

You should see a log line reporting the number of parsed documentation sections.
