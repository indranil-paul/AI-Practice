#!/bin/bash

set -e

PYTHON_VERSION="3.14.5"
VENV_NAME=".venv"

echo -e "\n"
echo "~~~~~~~~~~~~~~~"
echo "Setup Started!"
echo "~~~~~~~~~~~~~~~"

echo -e "\n-> Installing Python ${PYTHON_VERSION} (if not already installed)..."
pyenv install -s ${PYTHON_VERSION}

echo -e "\n-> Setting local Python version..."
pyenv local ${PYTHON_VERSION}

echo -e "\n-> Creating virtual environment..."
python -m venv ${VENV_NAME}

echo -e "\n-> Activating virtual environment..."
source ${VENV_NAME}/bin/activate

echo -e "\n-> Upgrading pip..."
pip install --upgrade pip

echo -e "\n-> Installing packages..."
pip install -r ./requirements.txt

echo -e "\n"
echo "~~~~~~~~~~~~~~~"
echo "Setup complete!"
echo "~~~~~~~~~~~~~~~"
echo -e "\nActivate the environment with: source ${VENV_NAME}/bin/activate"