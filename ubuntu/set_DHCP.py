import os
import subprocess

file_path = "/etc/netplan/50-cloud-init.yaml"
new_netplan_config = f"""
network:
  version: 2
  ethernets:
    enp6s18:
      dhcp4: true
"""

backup_filename = f"{file_path}.bak"

def check_file_and_permissions(file_path):
    if os.path.isfile(file_path):
        return os.access(file_path, os.R_OK | os.W_OK)
    return False

if __name__ == "__main__":
    # Make a backup of the current netplan configuration file before making changes
    subprocess.run(["sudo", "cp", file_path, backup_filename], check=True)
    try:
        if check_file_and_permissions(file_path):
            with open(file_path, "w") as f:
                f.write(new_netplan_config)
                subprocess.run(["sudo", "netplan", "apply"], check=True)
                subprocess.run(["sudo", "reboot", "now"], check=True)
        else:
            print(f"Cannot write to {file_path}. Check if the file exists and you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")