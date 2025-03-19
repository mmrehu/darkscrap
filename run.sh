#!/bin/bash

# Script to automate the execution of the darkweb.py script on Tails OS

# Ensure the script is running on Tails OS
if ! grep -q "Tails" /etc/os-release; then
    echo "This script is intended to run on Tails OS. Exiting."
    exit 1
fi

# Install Python and pip (if not already installed)
echo "Installing Python and pip..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# Verify Python and pip installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed."
    exit 1
fi

# Set up a virtual environment
VENV_DIR="$HOME/darkweb-venv"
echo "Creating a virtual environment at $VENV_DIR..."
python3 -m venv "$VENV_DIR"

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install Python dependencies in the virtual environment
echo "Installing Python dependencies..."
"$VENV_DIR/bin/pip" install --no-color --no-python-version-warning requests beautifulsoup4 urwid tqdm

# Check if the installation was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python dependencies. Check your network connection."
    exit 1
fi

# Ensure Tor is running
echo "Checking Tor service..."
if ! sudo service tor status | grep -q "active (running)"; then
    echo "Starting Tor service..."
    sudo service tor start
    sleep 5  # Wait for Tor to start
fi

# Check if Tor is running
if ! sudo service tor status | grep -q "active (running)"; then
    echo "Tor is not running. Please start Tor manually and try again."
    exit 1
fi

# Run the Python script using the virtual environment's Python
echo "Running the darkweb scraper..."
"$VENV_DIR/bin/python" darkweb.py

# Check if the Python script ran successfully
if [ $? -eq 0 ]; then
    echo "Darkweb scraper has completed. Check the results in darkweb_results.json and darkweb_results.csv."
else
    echo "Error: The darkweb scraper script failed to run."
    exit 1
fi

# Kill the Tor Browser to avoid conflicts
echo "Killing Tor Browser to avoid conflicts..."
if pgrep -f "tor-browser" > /dev/null; then
    pkill -f "tor-browser"
    sleep 2  # Wait for the process to terminate
fi

# Check if Tor Browser was successfully killed
if pgrep -f "tor-browser" > /dev/null; then
    echo "Warning: Failed to kill Tor Browser. Please close it manually."
else
    echo "Tor Browser has been successfully killed."
fi
