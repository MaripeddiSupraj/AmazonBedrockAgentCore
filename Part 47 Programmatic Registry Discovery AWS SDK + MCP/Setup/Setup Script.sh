#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "===================================================="
echo " Starting Amazon Linux 2023 Environment Setup "
echo "===================================================="

# 1. Update system packages safely
echo "--> Updating system packages..."
sudo dnf update -y

# 2. Install Python 3.11 and Git
#    NOTE: python3.11-pip does NOT exist in AL2023 repos - pip is bootstrapped via ensurepip
echo "--> Installing Python 3.11 and Git..."
sudo dnf install -y python3.11 git

# 3. Bootstrap pip for Python 3.11 using ensurepip (built into Python 3.11)
echo "--> Bootstrapping pip for Python 3.11..."
python3.11 -m ensurepip --upgrade

# 4. Upgrade pip itself
echo "--> Upgrading pip..."
python3.11 -m pip install --upgrade pip

# 5. Install AWS SDK + dependencies under Python 3.11
echo "--> Fetching latest Boto3 packages with Agent Registry support..."
python3.11 -m pip install --upgrade boto3 botocore requests uvicorn

# 6. Make python3.11 the default python3 for this user session
echo "--> Setting Python 3.11 as default..."
mkdir -p ~/.local/bin
ln -sf /usr/bin/python3.11 ~/.local/bin/python3
export PATH="$HOME/.local/bin:$PATH"

# Persist PATH for future sessions
grep -qxF 'export PATH="$HOME/.local/bin:$PATH"' ~/.bashrc || \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# 7. Verify installation success
echo "--> Verifying Python and Boto3 versions..."
python3.11 --version
python3.11 -c "import boto3; print('Boto3 Version:', boto3.__version__)"

echo "===================================================="
echo " Setup complete! Your AL2023 instance is ready. "
echo "===================================================="
