import os
import sys
import json
import yaml
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_swagger_json(url):
    print(f"Downloading Swagger spec from {url}")
    response = requests.get(url, verify=False)  # Disable SSL verification
    response.raise_for_status()
    return response.json()


def split_paths(openapi_dict, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for path, methods in openapi_dict.get("paths", {}).items():
        safe_path = path.strip("/").replace("/", "_") or "root"
        output_file = os.path.join(output_dir, f"{safe_path}.yaml")
        partial_doc = {
            "openapi": openapi_dict.get("openapi", "3.0.0"),
            "info": openapi_dict.get("info", {}),
            "paths": {path: methods}
        }
        with open(output_file, "w") as f:
            yaml.dump(partial_doc, f)

if __name__ == "__main__":
    env = sys.argv[1]
    # swagger_url = "http://localhost:5000/swagger/v1/swagger.json"
    swagger_url = "http://localhost:5001/swagger/v1/swagger.json"

    output_dir = f"./output/{env}"
    response = requests.get(swagger_url, verify=False)
    print(f"Downloading Swagger spec from {swagger_url}")
    openapi = download_swagger_json(swagger_url)
    split_paths(openapi, output_dir)
    print(f"YAMLs saved to: {output_dir}")
