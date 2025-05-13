import yaml
import os
import sys

# Take environment from command-line args
if len(sys.argv) != 2:
    print("Usage: python split_openapi.py [dev|qa|pt]")
    sys.exit(1)

env = sys.argv[1]

# Load Swagger YAML file
with open("swagger.yaml", "r") as f:
    openapi = yaml.safe_load(f)

# Prepare output directory
output_dir = f"MyApiProject/output/{env}"
os.makedirs(output_dir, exist_ok=True)

# Extract and write each API path to a separate file
for path, path_item in openapi.get("paths", {}).items():
    safe_path = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
    if not safe_path:
        safe_path = "root"
    
    out_file = os.path.join(output_dir, f"{safe_path}.yaml")
    path_yaml = {
        "openapi": openapi.get("openapi", "3.0.0"),
        "info": openapi.get("info", {}),
        "paths": {path: path_item}
    }
    
    with open(out_file, "w") as f:
        yaml.dump(path_yaml, f)

print(f"✅ Split {len(openapi.get('paths', {}))} paths into {output_dir}")
