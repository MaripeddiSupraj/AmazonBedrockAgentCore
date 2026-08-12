#!/bin/bash
set -euo pipefail

# ------------------------------------------------------------
# AgentCore CLI Preview Setup
# ------------------------------------------------------------
# The AgentCore CLI is installed via Node.js (npm).
# The CLI-generated agent runtime is Python-based and expects main.py.
# UV is added for clean Python environment management.
# ------------------------------------------------------------

echo "=== Installing Core Utilities ==="
sudo apt-get update -y
sudo apt-get install -y \
  curl \
  unzip \
  jq \
  git \
  ca-certificates \
  lsb-release

echo "=== Installing Node.js & NPM (Ubuntu Repository) ==="
sudo apt-get install -y nodejs npm

echo "=== Installing Python3 ==="
sudo apt-get install -y python3 python3-pip python3-venv

echo "=== Installing UV (Python Environment Manager) ==="
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "=== Installing AWS CLI v2 ==="
curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws

echo "=== Installing AgentCore CLI Preview ==="
sudo npm install -g @aws/agentcore

echo "=== Verifying Installations ==="
echo "Node: $(node -v)"
echo "NPM: $(npm -v)"
echo "Python: $(python3 --version)"
echo "Pip: $(pip3 --version)"
echo "UV: $(uv --version)"
echo "AWS: $(aws --version)"
echo "AgentCore CLI Version: $(agentcore --version 2>/dev/null || echo 'AgentCore CLI not found')"

echo "=== AgentCore CLI Preview Environment Ready ==="
