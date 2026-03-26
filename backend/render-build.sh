#!/usr/bin/env bash

echo "Installing Chromium..."

apt-get update || true
apt-get install -y chromium chromium-driver || true

echo "Done"
