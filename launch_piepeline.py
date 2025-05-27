import argparse
import shutil
import subprocess
import json
import os


def generate_telegraf_config():
    devices_path = os.path.join(os.path.dirname(__file__), 'devices.json')
    try:
        with open(devices_path, 'r') as f:
            devices = json.load(f)
            print(devices)
    except FileNotFoundError:
        print("devices.json not found.")
    except json.JSONDecodeError:
        print("devices.json is not a valid JSON file.")


def get_synthetic_telegraf_config():
    current_dir = os.dirname(__file__)
    synthetic_telegraf_config_path = os.path.join(current_dir, '_templates', '_telegraf.conf')
    current_telegraf_config_path = os.path.join(current_dir, 'telegraf','telegraf.conf')
    os.remove(current_telegraf_config_path)
    shutil.copy2(synthetic_telegraf_config_path, current_telegraf_config_path)


def start_pipeline(use_devices, use_synthetic):

    if use_synthetic:
        get_synthetic_telegraf_config()
        print("Starting the pipeline for synthetic data...")

    elif use_devices:
        print("Starting the pipeline for devices...")
        generate_telegraf_config()

    # Add your pipeline logic here
    print("Pipeline started (placeholder).")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start the pipeline.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--devices', action='store_true', help='Use devices')
    group.add_argument('--synthetic', action='store_true', help='Use synthetic data')
    args = parser.parse_args()
    # Default to devices if neither flag is set
    if not args.devices and not args.synthetic:
        args.devices = True
    start_pipeline(args.devices, args.synthetic)
