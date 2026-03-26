# #!/usr/bin/env bash

# echo "Installing Chromium..."

# apt-get update || true
# apt-get install -y chromium chromium-driver || true

# echo "Done"







#!/usr/bin/env bash

echo "Updating packages..."

apt-get update -y

echo "Installing Chromium + Driver..."

apt-get install -y chromium chromium-driver

echo "Checking installation..."

which chromium
which chromedriver

echo "Done"
