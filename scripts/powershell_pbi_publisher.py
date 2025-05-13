# -- coding: utf-8 --
import os
import sys
import shutil
import logging
import subprocess
import yaml
from datetime import datetime

PROGRAM_NAME = "Power BI Auto Publisher"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Folder and file definitions
input_foldername = 'input'
output_foldername = 'output'
log_foldername = 'logs'
config_foldername = 'config'
config_filename = 'config.yaml'
log_filename = f"{timestamp}_log.log"

# Paths
path_script = os.path.realpath(__file__)
path_project = os.path.dirname(os.path.dirname(path_script))
path_input = os.path.join(path_project, input_foldername)
path_output = os.path.join(path_project, output_foldername)
path_log_folder = os.path.join(path_project, log_foldername)
path_log = os.path.join(path_log_folder, log_filename)
path_config = os.path.join(path_project, config_foldername, config_filename)

# Ensure necessary folders exist
os.makedirs(path_input, exist_ok=True)
os.makedirs(path_output, exist_ok=True)
os.makedirs(path_log_folder, exist_ok=True)

# Logging setup
log_format = f"{PROGRAM_NAME}: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

# Load workspace name from config.yaml
if not os.path.exists(path_config):
    logging.error(f"Config file not found: {path_config}")
    sys.exit(1)

with open(path_config, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

workspace_name = config.get("workspace_name")
if not workspace_name:
    logging.error("Missing 'workspace_name' key in config.yaml.")
    sys.exit(1)

# Find PBIX files to process
pbix_files = [f for f in os.listdir(path_input) if f.endswith(".pbix")]
pbix_count = len(pbix_files)
logging.info(f"Found {pbix_count} PBIX file(s) to publish.")

if not pbix_files:
    logging.warning("No PBIX files found in input folder. Exiting.")
    sys.exit()

# Build PowerShell script as a single string
ps_script_lines = [
    'Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force',
    'Connect-PowerBIServiceAccount'
]

for pbix_file in pbix_files:
    input_file_path = os.path.join(path_input, pbix_file)
    report_name = os.path.splitext(pbix_file)[0]

    ps_script_lines.append(
        f'Write-Output "Publishing {report_name} ..."'
    )
    ps_script_lines.append(
        f'New-PowerBIReport -Path "{input_file_path}" -Workspace (Get-PowerBIWorkspace -Name "{workspace_name}") -ConflictAction CreateOrOverwrite'
    )

# Combine all PowerShell commands into one script block
powershell_script = "; ".join(ps_script_lines)

# Execute the PowerShell script
logging.info("Launching PowerShell to publish reports...")
result = subprocess.run(["powershell", "-Command", powershell_script], capture_output=True, text=True)

if result.returncode == 0:
    logging.debug(result.stdout)
    logging.info("All reports published successfully.")
else:
    logging.error(result.stderr)
    logging.error("Error while executing PowerShell command.")
    sys.exit(1)

# Move all published PBIX files to the output folder
for pbix_file in pbix_files:
    try:
        src = os.path.join(path_input, pbix_file)
        dst = os.path.join(path_output, pbix_file)
        shutil.move(src, dst)
        logging.info(f"Moved file to output: {pbix_file}")
    except Exception as e:
        logging.error(f"Error while moving '{pbix_file}': {e}")

logging.info("Publishing process completed.")
logging.info(f"Total files processed: {pbix_count}")