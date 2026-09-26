import os
import subprocess

file_path = "/etc/netplan/50-cloud-init.yaml"
new_ip_address = input("Enter the new IP address (with subnet, e.g., 192.168.10.50/24): ")
new_gateway = new_ip_address.rsplit('.', 1)[0] + '.1'
new_netplan_config = f"""
network:
  version: 2
  ethernets:
    enp6s18:
      addresses:
      - "{new_ip_address}"
      nameservers:
        addresses:
        - 1.1.1.1
        - 8.8.8.8
        search: []
      routes:
      - to: "default"
        via: "{new_gateway}"
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
        if not new_ip_address:
            raise ValueError("IP address cannot be empty.")
        elif '/' not in new_ip_address:
            raise ValueError("IP address must include the subnet (e.g., 192.168.10.50/24).")
        elif new_ip_address.count('.') != 3:
            raise ValueError("IP address must be in the format x.x.x.x/xx.")
        else:
            octets = new_ip_address.split('/')[0].split('.')
            if not all(o.isdigit() and 0 <= int(o) <= 255 for o in octets):
                raise ValueError("Each octet of the IP address must be between 0 and 255.")
            subnet = new_ip_address.split('/')[1]
            if not subnet.isdigit() or not 0 <= int(subnet) <= 32:
                raise ValueError("Subnet must be a number between 0 and 32.")

            
        if check_file_and_permissions(file_path):
            with open(file_path, "w") as f:
                f.write(new_netplan_config)
                subprocess.run(["sudo", "netplan", "apply"], check=True)
                subprocess.run(["sudo", "reboot", "now"], check=True)
        else:
            print(f"Cannot write to {file_path}. Check if the file exists and you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")
