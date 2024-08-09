import os
import subprocess
from pathlib import Path

# Constants
USERNAME = "likhon"
PASSWORD = "likhon"
SSH_DIR = Path(f"/home/{USERNAME}/.ssh")
AUTHORIZED_KEYS_FILE = SSH_DIR / "authorized_keys"

def check_command(cmd):
    """Run a command and exit if it fails."""
    result = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error: Command '{cmd}' failed with error: {result.stderr.strip()}")
        exit(1)
    return result.stdout.strip()

def install_openssh_server():
    """Update package list and install OpenSSH Server if not installed."""
    print("Updating package list...")
    check_command("sudo apt-get update")
    
    print("Checking if OpenSSH Server is installed...")
    if "openssh-server" in check_command("dpkg -l | grep openssh-server"):
        print("OpenSSH Server is already installed.")
    else:
        print("Installing OpenSSH Server...")
        check_command("sudo apt-get install -y openssh-server")

def setup_user():
    """Create a new user and set up password and sudo permissions."""
    print(f"Checking if user '{USERNAME}' exists...")
    if check_command(f"id {USERNAME}") != "":
        print(f"User '{USERNAME}' already exists.")
    else:
        print(f"Creating user '{USERNAME}'...")
        check_command(f"sudo adduser --gecos '' --disabled-password {USERNAME}")
        
        print(f"Setting password for user '{USERNAME}'...")
        check_command(f"echo '{USERNAME}:{PASSWORD}' | sudo chpasswd")
        
        print(f"Configuring passwordless sudo for user '{USERNAME}'...")
        check_command(f"echo '{USERNAME} ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/{USERNAME} > /dev/null")

def start_ssh_service():
    """Start and enable SSH service."""
    print("Starting SSH service...")
    if "active (running)" in check_command("sudo service ssh status"):
        print("SSH service is already running.")
    else:
        check_command("sudo service ssh start")

def setup_ssh_keys():
    """Add SSH public key to authorized_keys for passwordless login."""
    print("Setting up SSH keys...")
    SSH_DIR.mkdir(parents=True, exist_ok=True)
    check_command(f"chmod 700 {SSH_DIR}")
    
    if Path("~/.ssh/id_rsa.pub").expanduser().exists():
        check_command(f"cat ~/.ssh/id_rsa.pub | sudo tee {AUTHORIZED_KEYS_FILE} > /dev/null")
        check_command(f"sudo chown -R {USERNAME}:{USERNAME} {SSH_DIR}")
        check_command(f"chmod 600 {AUTHORIZED_KEYS_FILE}")
    else:
        print("Error: SSH public key not found. Please generate it using 'ssh-keygen'.")
        exit(1)

def get_ip_address():
    """Retrieve the IP address of the Codespace."""
    print("Retrieving IP address...")
    ip_address = check_command("curl -s ifconfig.me")
    return ip_address

def print_login_info(ip_address):
    """Print the login information for the user."""
    print("""
    ==============================
    GitHub Codespaces VPS Setup
    ==============================
    Login Information:
    Username: {username}
    Password: {password}
    SSH Command: ssh {username}@{ip_address}
    ==============================
    """.format(username=USERNAME, password=PASSWORD, ip_address=ip_address))

def main():
    """Main function to run the setup."""
    try:
        install_openssh_server()
        setup_user()
        start_ssh_service()
        setup_ssh_keys()
        ip_address = get_ip_address()
        print_login_info(ip_address)
    except Exception as e:
        print(f"Fatal Error Occurred:\n{str(e)}\nAborting...")
        exit(1)

if __name__ == "__main__":
    main()
