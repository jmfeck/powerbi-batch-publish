# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 12:58:46 2025

@author: HH-FECK
"""

import os
import sys
import time
import shutil
import logging
import pyautogui
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "Power BI Auto Publisher"

# Timestamp for log and filenames
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Folder and file names
input_foldername = 'input'
output_foldername = 'output'
assets_foldername = 'assets'
log_foldername = 'logs'
log_filename = f"{timestamp}_log.log"

# Define absolute paths
path_script = os.path.realpath(__file__)
path_project = os.path.dirname(os.path.dirname(path_script))
path_input = os.path.join(path_project, input_foldername)
path_output = os.path.join(path_project, output_foldername)
path_assets = os.path.join(path_project, assets_foldername)
path_log_folder = os.path.join(path_project, log_foldername)
path_log = os.path.join(path_log_folder, log_filename)

# Ensure folders exist
os.makedirs(path_input, exist_ok=True)
os.makedirs(path_output, exist_ok=True)
os.makedirs(path_log_folder, exist_ok=True)

# Logging setup
log_format = f"{PROGRAM_NAME}: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

def find_button_with_retries(image_path, max_attempts=30, wait_between=10):
    for attempt in range(1, max_attempts + 1):
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.90)
        if location:
            logging.info(f"Found '{image_path}' on attempt {attempt}.")
            return location
        else:
            logging.warning(f"Attempt {attempt}: '{image_path}' not found. Retrying in {wait_between}s...")
            time.sleep(wait_between)
    logging.error(f"Failed to locate '{image_path}' after {max_attempts} attempts.")
    return None

# Start of the process
logging.info("Starting Power BI publishing process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Scanning for .pbix files...")

pbix_files = [f for f in os.listdir(path_input) if f.endswith(".pbix")]
pbix_count = len(pbix_files)
logging.info(f"Found {pbix_count} file(s) to process.")

if not pbix_files:
    logging.warning("No PBIX files found. Exiting.")
    sys.exit()

for pbix_file in pbix_files:
    try:
        input_file_path = os.path.join(path_input, pbix_file)
        output_file_path = os.path.join(path_output, pbix_file)

        logging.info(f"Opening: {pbix_file}")
        os.startfile(input_file_path)
        time.sleep(60)  # wait for Power BI to open and load
        
        # Click "Publish"
        publish_button_path = os.path.join(path_assets, 'publish_button.png')
        publish_button = find_button_with_retries(publish_button_path)
        if publish_button:
            pyautogui.click(publish_button)
            time.sleep(10)
        else:
            raise Exception("Publish button not found.")


        # save_button_path = os.path.join(path_assets, 'save_button.png')
        # save_button = find_button_with_retries(save_button_path, max_attempts=3)
        # if save_button:
        #     pyautogui.click(save_button)
        #     logging.info("Confirmed 'Save'.")
        #     time.sleep(5)
        # else:
        #     logging.info("No 'Save' confirmation detected. Proceeding...")            

        # Select workspace name
        workspace_name_path = os.path.join(path_assets, 'workspace_name.png')
        workspace_name = find_button_with_retries(workspace_name_path, max_attempts=3)
        if workspace_name:
            pyautogui.click(workspace_name)
            time.sleep(10)
        else:
            raise Exception("Workspace name not found.")
            
        # Click select for workspace
        select_button_path = os.path.join(path_assets, 'select_button.png')
        select_button = find_button_with_retries(select_button_path, max_attempts=3)
        if select_button:
            pyautogui.click(select_button)
            time.sleep(10)
        else:
            raise Exception("Select button not found.")
            
        # Click "Replace"
        replace_button_path = os.path.join(path_assets, 'replace_button.png')
        replace_button = find_button_with_retries(replace_button_path, max_attempts=3)
        if replace_button:
            pyautogui.click(replace_button)
            logging.info("Confirmed 'Replace'.")
            time.sleep(120)  # publishing time
        else:
            logging.info("No 'Replace' confirmation detected. Proceeding...")
            
        # Click "Got it"
        gotit_button_path = os.path.join(path_assets, 'gotit_button.png', max_attempts=15)
        gotit_button = find_button_with_retries(gotit_button_path)
        if replace_button:
            pyautogui.click(gotit_button)
            logging.info("Confirmed 'Got it'.")
            time.sleep(10)
        else:
            raise Exception("No 'Got it' confirmation detected.")

        # Click "Save"
        pyautogui.hotkey('ctrl', 's')
        logging.info("Saved Power BI.")
        time.sleep(30)

        # save_button_path = os.path.join(path_assets, 'save_button.png')
        # save_button = find_button_with_retries(save_button_path)
        # if replace_button:
        #     pyautogui.click(save_button)
        #     logging.info("Confirmed 'Save'.")
        #     time.sleep(5)
        # else:
        #     logging.info("No 'Save' confirmation detected. Proceeding...")

        # Close Power BI
        pyautogui.hotkey('alt', 'f4')
        logging.info("Closed Power BI.")
        time.sleep(10)

        # Move file to archive
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        shutil.move(input_file_path, output_file_path)
        logging.info(f"Moved to archive: {pbix_file}")

    except Exception as e:
        logging.error(f"Failed to publish '{pbix_file}': {e}")

logging.info("Publishing process completed.")
logging.info(f"Total files processed: {pbix_count}")