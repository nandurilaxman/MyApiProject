# API Swagger Extraction with GitHub Actions

This project demonstrates how to automate the process of downloading and extracting API paths from a Swagger JSON file using **GitHub Actions**, **.NET**, and **Python**. We use GitHub Actions for Continuous Integration (CI) and Continuous Deployment (CD), and Python to split the Swagger JSON into multiple YAML files based on the environment (e.g., `dev`, `qa`, `prod`).

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [How It Works](#how-it-works)
5. [Steps to Set Up](#steps-to-set-up)
6. [How to Run](#how-to-run)
7. [GitHub Actions Workflows](#github-actions-workflows)
8. [How to Use](#how-to-use)

## Overview

In this project:

* A **.NET API** exposes endpoints that are documented using Swagger.
* The **Python script** (`split_openapi.py`) extracts the paths from the Swagger documentation and saves them into separate YAML files for each environment.
* GitHub Actions workflows automate the entire process of building the .NET API, running it locally, and extracting the Swagger paths.

## Prerequisites

Before getting started, you need the following tools and setups:

1. **.NET SDK** (version 8.0 or higher)

   * Install from [here](https://dotnet.microsoft.com/download).
2. **Python** (version 3.9 or higher)

   * Install from [here](https://www.python.org/downloads/).
3. **GitHub Account** to run the workflows and interact with the repository.

## Project Structure

Here’s the basic structure of the project:

```
MyApiProject/
│
├── Scripts/
│   └── split_openapi.py      # Python script to extract APIs and save to YAML
│
├── MyApi/
│   ├── Controllers/
│   │   └── WeatherForecastController.cs  # Example controller
│   ├── Program.cs                    # .NET entry point and Swagger setup
│   ├── MyApi.csproj                  # .NET project file
│
├── .github/
│   └── workflows/
│       ├── main.yml                 # Main workflow to trigger reusable workflows
│       └── extract-swagger-apis.yml # Reusable workflow to extract API paths
├── README.md                       # Project documentation
```

### Key Files:

* **`split_openapi.py`**: Python script that downloads the Swagger JSON, splits it into individual API YAML files, and saves them.
* **`Program.cs`**: The entry point for the .NET application that configures and serves the Swagger documentation.
* **GitHub Workflows**: `.github/workflows/main.yml` and `.github/workflows/extract-swagger-apis.yml` define CI/CD pipelines.

## How It Works

### Step 1: Build the .NET API

The first part of the process is building and running a simple **.NET API** that is documented using **Swagger**. The API exposes some basic endpoints (e.g., `GET /weatherforecast`) and the Swagger documentation is available at `http://localhost:5001/swagger`.

### Step 2: Extract Swagger API Paths

Once the API is running locally, we use the Python script (`split_openapi.py`) to:

1. Download the Swagger JSON from `http://localhost:5001/swagger/v1/swagger.json`.
2. Split the API paths from the JSON into separate YAML files, each representing different environment configurations (e.g., `dev`, `qa`, `prod`).

### Step 3: GitHub Actions Automation

To automate the entire process, we use **GitHub Actions**:

* A **main workflow** triggers the building of the .NET API and the running of the Python script.
* A **reusable workflow** (`extract-swagger-apis.yml`) handles the API extraction logic. This can be reused for different environments like `dev`, `qa`, and `prod`.

## Steps to Set Up

1. **Clone the Repository**:
   Clone this repository to your local machine or to your GitHub account.

   ```bash
   git clone https://github.com/yourusername/MyApiProject.git
   cd MyApiProject
   ```

2. **Install Dependencies**:

   * Install the **.NET SDK**:
     Follow the [official instructions](https://dotnet.microsoft.com/download) to install the .NET SDK on your machine.
   * Install **Python** and dependencies:

     ```bash
     python -m pip install requests pyyaml
     ```

3. **Set Up the .NET API**:

   * Open the `Program.cs` file and make sure Swagger is configured as shown:

     ```csharp
     builder.Services.AddSwaggerGen(c =>
     {
         c.SwaggerDoc("v1", new OpenApiInfo { Title = "My API", Version = "v1" });
         c.SerializeAsV2 = true; // Generates YAML
     });
     ```

4. **Add Your Python Script**:
   The script `split_openapi.py` will be responsible for splitting the Swagger API into multiple YAML files:

   ```python
   import requests
   import yaml
   import os
   import sys

   def download_swagger_json(url):
       response = requests.get(url)
       response.raise_for_status()
       return response.json()

   def split_api_paths(swagger_json, environment):
       output_dir = f"output/{environment}"
       os.makedirs(output_dir, exist_ok=True)

       for path, details in swagger_json['paths'].items():
           yaml_data = {
               'paths': {path: details}
           }
           filename = os.path.join(output_dir, f"{path.strip('/').replace('/', '-')}.yaml")
           with open(filename, 'w') as file:
               yaml.dump(yaml_data, file)

   if __name__ == "__main__":
       environment = sys.argv[1]
       swagger_url = 'http://localhost:5001/swagger/v1/swagger.json'
       swagger_json = download_swagger_json(swagger_url)
       split_api_paths(swagger_json, environment)
   ```

5. **GitHub Actions Workflow**:

   * **Main Workflow**: The main workflow will trigger the reusable workflow (`extract-swagger-apis.yml`), passing the required environment (`dev`, `qa`, `prod`):

     ```yaml
     name: Deploy API and Extract Swagger

     on:
       push:
         branches:
           - main

     jobs:
       call-extract-apis:
         uses: ./path/to/extract-swagger-apis.yml
         with:
           environment: 'dev'
     ```

## How to Run

1. **Run Locally**:
   If you want to run everything locally, start the .NET API first:

   ```bash
   dotnet run
   ```

   Then, run the Python script to extract the API paths:

   ```bash
   python3 Scripts/split_openapi.py dev
   ```

2. **GitHub Actions**:
   Whenever you push changes to the `main` branch, the **GitHub Actions workflow** will automatically run. It will:

   1. Build and run the .NET API.
   2. Call the Python script to extract API paths.
   3. Upload the resulting YAML files as GitHub artifacts for further use.

   You can monitor the progress in the **Actions** tab on your GitHub repository.

## GitHub Actions Workflows

### Main Workflow (`main.yml`):

This is the entry point for running the GitHub Actions workflow. It triggers the reusable workflow to extract API paths.

```yaml
name: Deploy API and Extract Swagger

on:
  push:
    branches:
      - main

jobs:
  call-extract-apis:
    uses: ./path/to/extract-swagger-apis.yml
    with:
      environment: 'dev'
```

### Reusable Workflow (`extract-swagger-apis.yml`):

This reusable workflow builds the .NET API, runs the Python script to extract Swagger APIs, and uploads the extracted YAML files as artifacts.

```yaml
name: Extract APIs from Swagger

on:
  workflow_call:
    inputs:
      environment:
        description: 'The environment for the build (e.g., dev, qa, prod)'
        required: true
        type: string

jobs:
  extract-apis:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up .NET SDK
        uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '8.0.x'

      - name: Restore and build the .NET project
        run: |
          dotnet restore
          dotnet build --no-restore
          nohup dotnet run --urls "http://0.0.0.0:5001" &

      - name: Set up Python 3.9
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests pyyaml

      - name: Download and split Swagger JSON
        run: |
          python3 Scripts/split_openapi.py ${{ inputs.environment }}

      - name: Upload API YAML artifacts
        uses: actions/upload-artifact@v3
        with:
          name: api-yaml-files
          path: output/*.yaml
```

## How to Use

1. Push changes to your repository, and GitHub Actions will trigger the workflows.
2. After the workflows run, check the **Artifacts** tab for the uploaded YAML files.
