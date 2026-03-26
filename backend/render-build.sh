#!/usr/bin/env bash

echo "Installing Chromium..."

apt-get update
apt-get install -y chromium chromium-driver

echo "Chromium installed successfully"
