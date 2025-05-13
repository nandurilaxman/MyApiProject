import os
import sys
import subprocess
import yaml

# Get environment from CLI args
env = sys.argv[1] if len(sys.argv) > 1 else "dev"

# Paths
dll_path = "bin/Debug/net8.0/MyApi.dll"  # Update path if needed
swagger_output_file = "swagger.yaml"
api_version = "v1"

# Step 1: Generate swagger.yaml using dotnet CLI
print(f"📦 Generating Swagger YAML from {dll_path}...")
try:
    subprocess.run([
        "dotnet", "swagger", "tofile",
        "--output", swagger_output_file,
        dll_path, api_version
    ], check=True)
    print("✅ Swagger YAML generated.")
except subprocess.CalledProcessError as e:
    print("❌ Failed to generate Swagger YAML:", e)
    sys.exit(1)

# Step 2: Load YAML
print("📖 Loading Swagger YAML...")
with open(swagger_output_file, "r") as f:
    openapi = yaml.safe_load(f)

# Step 3: Split by path
output_dir = f"MyApiProject/output/{env}"
os.makedirs(output_dir, exist_ok=True)

print(f"✂️ Splitting paths into separate files in '{output_dir}'...")
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

print(f"✅ Done! {len(openapi['paths'])} path(s) written to {output_dir}")
