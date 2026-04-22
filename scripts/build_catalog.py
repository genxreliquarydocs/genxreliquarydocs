import os
import re

METADATA_DIR = "catalog/metadata/"
CATALOG_FILE = "CATALOG.md"

def parse_metadata(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Simple regex to grab frontmatter values
    data = {
        "id": os.path.splitext(os.path.basename(file_path))[0],
        "name": re.search(r"name:\s*(.*)", content).group(1),
        "tier": re.search(r"tier:\s*(.*)", content).group(1),
        "aura": re.search(r"aura:\s*(.*)", content).group(1),
    }
    return data

def build():
    items = []
    for filename in os.listdir(METADATA_DIR):
        if filename.endswith(".md"):
            items.append(parse_metadata(os.path.join(METADATA_DIR, filename)))

    # Sort by ID
    items.sort(key=lambda x: x['id'])

    with open(CATALOG_FILE, 'w') as f:
        f.write("# GenXReliquary Catalog\n\n")
        f.write("| ID | Tier | Name | Aura | Link |\n")
        f.write("| :--- | :---: | :--- | :--- | :--- |\n")
        for i in items:
            f.write(f"| `{i['id']}` | **{i['tier']}** | {i['name']} | {i['aura']} | [view]({METADATA_DIR}{i['id']}.md) |\n")

if __name__ == "__main__":
    build()
