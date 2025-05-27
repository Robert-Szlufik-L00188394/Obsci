import argparse
import shutil
import subprocess
import json
import os


def generate_telegraf_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    devices_path = os.path.join(current_dir, 'devices.json')
    base_config_path = os.path.join(current_dir, '_templates', 'base_telegraf.conf')
    telegraf_config_path = os.path.join(current_dir, 'telegraf', 'telegraf.conf')

    # Load base Telegraf config
    try:
        with open(base_config_path, 'r') as f:
            base_config = f.read()
    except FileNotFoundError:
        print("Base Telegraf config not found in _templates.")
        return

    # Load devices.json
    try:
        with open(devices_path, 'r') as f:
            devices = json.load(f)
    except FileNotFoundError:
        print("devices.json not found.")
        return
    except json.JSONDecodeError:
        print("devices.json is not a valid JSON file.")
        return

    # SNMP input template
    snmp_template = '''
                    [[inputs.snmp]]
                      agents = ["udp6://{ip}:161"]
                      version = "{version}"
                      community = "{community}"
                      name = "snmp.{name}"
                    
                      [[inputs.snmp.field]]
                        name = "sysUpTime"
                        oid = "1.3.6.1.2.1.1.3.0"
                        is_tag = false
                    
                      [[inputs.snmp.field]]
                        name = "sysName"
                        oid = "1.3.6.1.2.1.1.5.0"
                        is_tag = true
                    '''

    required_keys = {"device_id", "ip", "community", "version"}
    snmp_blocks = []
    for device in devices:
        if not required_keys.issubset(device):
            print(f"Skipping invalid device entry: {device}")
            continue
        print(f"Including device: {device['device_id']} at {device['ip']}")
        snmp_block = snmp_template.format(
            ip=device['ip'],
            version=device['version'],
            community=device['community'],
            name=device['device_id']
        )
        snmp_blocks.append(snmp_block)

    try:
        with open(telegraf_config_path, 'w') as f:
            f.write(base_config.strip() + '\n\n' + '\n\n'.join(snmp_blocks))
        print(f"Generated telegraf.conf for {len(snmp_blocks)} valid device(s).")
    except Exception as e:
        print(f"Error writing telegraf config: {e}")


def get_synthetic_telegraf_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    synthetic_telegraf_config_path = os.path.join(current_dir, '_templates', 'http_telegraf.conf')
    current_telegraf_config_path = os.path.join(current_dir, 'telegraf', 'telegraf.conf')
    os.remove(current_telegraf_config_path)
    shutil.copy2(synthetic_telegraf_config_path, current_telegraf_config_path)


def start_pipeline(use_devices, use_synthetic):
    if use_devices:
        print("Generating config for telegraf from devices...")
        generate_telegraf_config()
    elif use_synthetic:
        print("Generating config for synthetic http api...")
        get_synthetic_telegraf_config()


    try:
        telegraf_config_path = os.path.join(os.path.dirname(__file__), 'telegraf', 'telegraf.conf')
        with open(telegraf_config_path, 'r') as f:
            print(f"Telegraf config loaded from {telegraf_config_path}")
            content = f.read()
            print(f'{content}')
    except FileNotFoundError:
        print(f"Telegraf config file not found at {telegraf_config_path}. Please check the path.")
        return

    print("Pipeline starting...")
    # subprocess.run(['docker', 'compose', 'up', '-d'], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start the pipeline.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--devices', action='store_true', help='Use devices')
    group.add_argument('--synthetic', action='store_true', help='Use synthetic data')
    args = parser.parse_args()
    # Default to devices if neither flag is set
    if not args.devices and not args.synthetic:
        args.synthetic = True
    start_pipeline(args.devices, args.synthetic)
