#!/bin/bash

# Update package list and install SSH server
sudo apt-get update
sudo apt-get install -y openssh-server

# Create a new user with the username 'likhon'
username="likhon"
password="likhon"

# Add the user and set the password
sudo adduser --gecos "" --disabled-password $username
echo "$username:$password" | sudo chpasswd

# Allow the new user to use sudo without a password
echo "$username ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$username

# Start and enable SSH service
sudo systemctl enable ssh
sudo systemctl start ssh

# Get the IP address of the Codespace
ip_address=$(curl -s ifconfig.me)

# Show the login information
echo "=============================="
echo "GitHub Codespaces VPS Setup"
echo "=============================="
echo "Login Information:"
echo "Username: $username"
echo "Password: $password"
echo "SSH Command: ssh $username@$ip_address"
echo "=============================="