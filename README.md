# Power BI Batch Publisher

📘 [Versão em Português (Brasil)](README.pt-BR.md)

---

This repository contains a Python/PowerShell-based tool that automates the publishing of `.pbix` files to the Power BI Service using PowerShell commands.

It is designed for Windows and is ideal for scenarios where you regularly publish multiple reports and want to avoid repetitive manual steps.

## Overview

- Place your `.pbix` files in the `input/` folder.
- Define the Power BI workspace in the `config/config.yaml` file.
- Run the tool using the batch file or directly via Python.
- The script logs in through the browser (not a service principal).
- It publishes each `.pbix` using its filename as the report name.
- Published files are moved to the `output/` folder.

## Folder Structure

    powerbi-batch-publisher/
    ├── input/                              Place PBIX files here
    ├── output/                             Published files are moved here
    ├── logs/                               Logs from execution
    ├── scripts/
    │   └── main.py                         Main script
    ├── config/
    │   └── config.yaml                     Set your workspace name here
    ├── run_powerbi_batch_publish.bat    Batch runner
    ├── requirements.txt
    └── README.md

## Setup Instructions

### 1. Clone the repository and install Python dependencies

    git clone https://github.com/jmfeck/powerbi-batch-publisher.git
    cd powerbi-batch-publisher
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

### 2. Install the Power BI PowerShell module

Open **PowerShell as Administrator** and run:

    Install-Module -Name MicrosoftPowerBIMgmt -Scope CurrentUser

During installation, you may be prompted to:

- **Install NuGet** — respond with `Y` to proceed.
- **Trust the PSGallery repository** — respond with `Y` to confirm.

> This module is required to publish `.pbix` files via script using PowerShell.

### 3. Confirm the installation

To verify that the module was installed correctly, run:

    Get-Module -ListAvailable MicrosoftPowerBIMgmt

You should see output like:

    ModuleType Version    Name                      ExportedCommands
    ---------- -------    ----                      ----------------
    Script     1.X.X      MicrosoftPowerBIMgmt      {Connect-PowerBIServiceAccount, ...}

If nothing is returned, the module did not install correctly. Try again as Administrator.

### 4. Set the workspace name

Edit the `config/config.yaml` file and define your target workspace:

    workspace_name: "YOUR_WORKSPACE_NAME"

You can find the name of your workspace in the Power BI Service URL or UI. It must match exactly.

### 5. Add PBIX files

Place all `.pbix` files you want to publish into the `input/` folder.  
Each report will be published using the **exact filename**, so be precise and intentional with naming.

### 6. Run the script

You can run the tool in two ways:

Using the batch file:

    run_powerbi_batch_publish.bat

Or directly via Python:

    python scripts/main.py

## What the Script Does

- Scans the `input/` folder for `.pbix` files.
- Builds a PowerShell command sequence that:
  - Sets execution policy to `Bypass` (required on some corporate systems).
  - Logs in to Power BI via browser (you will be prompted to sign in).
  - Publishes each `.pbix` file to the defined workspace.
- After publishing:
  - The script prints out report links for verification.
  - Each published file is moved to the `output/` folder.
- Reports with the same name will be **overwritten**.

## Reinforcing Notes

- This tool has only been tested on **Windows**.
- Authentication is handled via interactive browser login (not service accounts).
- The published report name is **exactly the same** as the `.pbix` filename.
- In real-world usage, this tool reduced a 30–60 minute manual publishing process (for 12 reports) to **under 3 minutes**.
