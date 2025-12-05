#!/bin/bash

echo "==============================================="
echo "☁️ INTELLIGENT CLIMATE CONTROL SETUP SCRIPT ☁️"
echo "==============================================="

# .venv name
VENV_NAME="CLIMATECRTL"

# Update and install system dependencies
echo "- Updating system and installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv i2c-tools libgpiod-dev 

# Creating virtual environment
echo "- Creating virtual environment: $VENV_NAME"
python3 -m venv $VENV_NAME

# Activate virtual environment
echo "- Activating virtual environment..."
source $VENV_NAME/bin/activate

# Installing required Python libraries
echo "- Installing Python libraries from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Granting GPIO/I2C permissions
    echo "- Granting GPIO/I2C permissions to the current user..."
    sudo usermod -a -G gpio $USER
    sudo usermod -a -G i2c $USER
    
    # Check installations
    echo "- Verifying installations..."
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    echo "Installed packages:"
    pip list

    echo " "
    echo "========================================================"
    echo "✅ INSTALLATION COMPLETED!"
    echo "The virtual environment '$VENV_NAME' has been created and the libraries installed."
    echo " "
    echo "HOW TO USE:"
    echo "1. To activate the environment, run:"
    echo "   source $VENV_NAME/bin/activate"
    echo "2. To run the project, use (after activation):"
    echo "   python main.py"
    echo " "
    echo "⚠️ Important: You MUST restart or log off/log on for the new permissions (GPIO/I2C) to take effect."
    echo "========================================================"
else
    echo "ERROR: The requirements.txt file was not found. Aborting installation."
fi