#!/bin/bash

# Variables
username="likhon"
password="likhon"

# Function to check the status of a command and exit if it fails
check_command() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed. Exiting."
        exit 1
    fi
}

# Update package list and install SSH server
echo "Updating package list..."
sudo apt-get update
check_command "apt-get update"

echo "Installing OpenSSH Server..."
sudo apt-get install -y openssh-server
check_command "apt-get install openssh-server"

# Create a new user with the username 'likhon'
echo "Creating user '$username'..."
sudo adduser --gecos "" --disabled-password $username
check_command "adduser"

# Set the user password
echo "Setting password for user '$username'..."
echo "$username:$password" | sudo chpasswd
check_command "chpasswd"

# Allow the new user to use sudo without a password
echo "Configuring passwordless sudo for user '$username'..."
echo "$username ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$username > /dev/null
check_command "tee /etc/sudoers.d/$username"

# Start and enable SSH service
echo "Starting SSH service..."
if ! sudo service ssh status > /dev/null 2>&1; then
    sudo service ssh start
    check_command "service ssh start"
else
    echo "SSH service is already running."
fi

# Add SSH public key to authorized_keys for passwordless login
echo "Setting up SSH keys..."
mkdir -p /home/$username/.ssh
chmod 700 /home/$username/.ssh
if [ -f ~/.ssh/id_rsa.pub ]; then
    cat ~/.ssh/id_rsa.pub | sudo tee /home/$username/.ssh/authorized_keys > /dev/null
    check_command "tee /home/$username/.ssh/authorized_keys"
    sudo chown -R $username:$username /home/$username/.ssh
    chmod 600 /home/$username/.ssh/authorized_keys
else
    echo "Error: SSH public key not found. Please generate it using 'ssh-keygen'."
    exit 1
fi

# Get the IP address of the Codespace
echo "Retrieving IP address..."
ip_address=$(curl -s ifconfig.me)
check_command "curl ifconfig.me"

# Show the login information
echo "=============================="
echo "GitHub Codespaces VPS Setup"
echo "=============================="
echo "Login Information:"
echo "Username: $username"
echo "Password: $password"
echo "SSH Command: ssh $username@$ip_address"
echo "=============================="