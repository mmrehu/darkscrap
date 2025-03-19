#!/bin/bash

# Script to automate the execution of the darkweb.py script on Tails OS

# Ensure the script is running on Tails OS
if ! grep -q "Tails" /etc/os-release; then
    echo "This script is intended to run on Tails OS. Exiting."
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Install Python dependencies (only if not already installed)
echo "Installing Python dependencies..."
pip3 install requests beautifulsoup4 urwid tqdm

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

# Run the Python script
echo "Running the darkweb scraper..."
python3 darkweb.py

# Check if
