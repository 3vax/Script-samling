#!/bin/bash

# Get system type
for lines in $(cat /etc/os-release); do
    if [[ $lines == "ID="* ]]; then
        ID=$(echo $lines | cut -d'=' -f2)
        break
    fi
done
echo "System type: $ID"

# Package manager based on system type
if [[ $ID == "ubuntu" OR $ID == "debian" ]]; then
    package_manager="apt"
elif [[ $ID == "fedora" OR $ID == "centos" OR $ID == "rhel" ]]; then
    package_manager="dnf"
elif [[ $ID == "arch" ]]; then
    package_manager="pacman"
else
    echo "Unsupported system type: $ID"
    exit 1
fi

# Update and upgrade the system¨
echo "Updating and upgrading the system..."
sudo $package_manager update && sudo $package_manager upgrade -y

# Install xrdp
echo "Installing XFCE and xrdp..."
sudo $package_manager install xfce4 xfce4-goodies -y
sudo $package_manager install xrdp -y

# Enable and start xrdp service
echo "Enabling and starting xrdp service..."
sudo systemctl start xrdp
sudo systemctl enable xrdp