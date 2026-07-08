import sys
import os
import re
import logging
from mcp.server.fastmcp import FastMCP

# Setup logging (FastMCP handles redirecting stdio safely)
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("genlayer-docs-mcp")

# Create FastMCP server instance
mcp = FastMCP("genlayer-docs")

# Get path of the bundled documentation file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCS_PATH = os.path.join(SCRIPT_DIR, "genlayer-docs.txt")
DOCS_PATH = os.environ.get("GENLAYER_DOCS_PATH", DEFAULT_DOCS_PATH)

class GenLayerDocsDB:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sections = []
        self.sections_by_title = {}
        self.load_and_parse()

    def load_and_parse(self):
        logger.info(f"Loading GenLayer documentation from: {self.file_path}")
        if not os.path.exists(self.file_path):
            logger.error(f"Documentation file not found at {self.file_path}")
            return

        active_headers = {}
        current_section = None
        
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
        except Exception as e:
            logger.error(f"Failed to read file: {e}")
            return

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            # Detect Markdown headers
            if stripped.startswith('#'):
                if current_section:
                    self.sections.append(current_section)
                
                level = len(stripped) - len(stripped.lstrip('#'))
                title = stripped.lstrip('#').strip()
                
                # Update hierarchy breadcrumbs
                active_headers[level] = title
                for k in list(active_headers.keys()):
                    if k > level:
                        del active_headers[k]
                
                hierarchy = [active_headers[k] for k in sorted(active_headers.keys())]
                hierarchy_str = " > ".join(hierarchy)
                
                current_section = {
                    'title': title,
                    'level': level,
                    'hierarchy': hierarchy_str,
                    'full_header': stripped,
                    'content_lines': [],
                    'start_line': line_num
                }
            else:
                if current_section is not None:
                    current_section['content_lines'].append(line)
                    
        if current_section:
            self.sections.append(current_section)

        # Process and clean contents
        for s in self.sections:
            s['content'] = ''.join(s['content_lines']).strip()
            del s['content_lines']
            
            # Index by title (case-insensitive for flexible lookups)
            self.sections_by_title[s['title'].lower()] = s

        logger.info(f"Successfully parsed {len(self.sections)} document sections.")

    def search(self, query, top_k=5):
        query_words = [w.lower() for w in re.findall(r'\w+', query)]
        if not query_words:
            return []
            
        scored_results = []
        for s in self.sections:
            score = 0
            title_lower = s['title'].lower()
            hierarchy_lower = s['hierarchy'].lower()
            content_lower = s['content'].lower()
            
            for word in query_words:
                if word in title_lower:
                    score += 20  # Strong match for direct title
                if word in hierarchy_lower:
                    score += 10  # Match in breadcrumbs
                if word in content_lower:
                    # Match in body content
                    occurrences = content_lower.count(word)
                    score += min(occurrences, 10)  # Limit weight to avoid keyword stuffing
                    
            if score > 0:
                scored_results.append((score, s))
                
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_results[:top_k]]

    def get_section(self, title):
        return self.sections_by_title.get(title.lower())

    def get_all_sections(self):
        return [
            {
                "title": s["title"],
                "hierarchy": s["hierarchy"],
                "level": s["level"],
                "start_line": s["start_line"]
            }
            for s in self.sections
        ]

# Instantiate DB
db = GenLayerDocsDB(DOCS_PATH)

@mcp.tool()
def search_docs(query: str, top_k: int = 5) -> str:
    """Search the GenLayer documentation for relevant sections matching a query.
    Returns the top matching sections with their hierarchical titles and full content.
    """
    results = db.search(query, top_k)
    if not results:
        return "No matching documentation sections found."
        
    formatted_results = []
    for s in results:
        formatted_results.append(
            f"### {s['hierarchy']} (Line {s['start_line']})\n\n{s['content']}\n\n---"
        )
        
    return "\n\n".join(formatted_results)

@mcp.tool()
def get_section(title: str) -> str:
    """Retrieve the full content of a specific documentation section by its exact title
    (e.g., 'Optimistic Democracy' or 'Economic Model').
    """
    section = db.get_section(title)
    if not section:
        return f"Error: Section '{title}' not found. Use list_sections to see all available headings."
        
    return f"### {section['hierarchy']} (Line {section['start_line']})\n\n{section['content']}"

@mcp.tool()
def list_sections() -> str:
    """List all section titles and headings available in the GenLayer documentation."""
    sections = db.get_all_sections()
    lines = []
    for s in sections:
        indent = "  " * (s["level"] - 1)
        lines.append(f"{indent}- {s['title']} (Line {s['start_line']})")
        
    return "\n".join(lines)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
