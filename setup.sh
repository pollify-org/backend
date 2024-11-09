#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Check for sqlite3 and install if necessary
if ! command -v sqlite3 &> /dev/null; then
    echo "sqlite3 is not installed. Installing it now..."
    sudo apt update
    sudo apt install sqlite3 -y
else
    echo "sqlite3 is already installed."
fi

# Check if Python 3 and venv are installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3."
    exit 1
fi
if ! python3 -m venv --help &> /dev/null; then
    echo "Python venv module is not installed. Installing it now..."
    sudo apt install python3-venv -y
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Uninstall all currently installed packages in the virtual environment
if pip freeze | grep -q .; then
  pip freeze | xargs pip uninstall -y
else
  echo "No packages to uninstall."
fi

# Determine the correct requirements file based on the environment
REQUIREMENTS_FILE="requirements.txt"
if [ -f ".env" ]; then
  source .env
  if [ "$ENV_STATE" == "dev" ]; then
    REQUIREMENTS_FILE="requirements-dev.txt"
  fi
fi

# Install the required packages
pip install -r $REQUIREMENTS_FILE
echo "Using requirements file: $REQUIREMENTS_FILE"
echo "Dependencies installed successfully."

# Setup SQLite database if it doesn't exist
DB_NAME="dev.db"
if [ ! -f "$DB_NAME" ]; then
    echo "Creating SQLite database: $DB_NAME"
    sqlite3 $DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS sample_table (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);
EOF
    echo "Database $DB_NAME created successfully."
else
    echo "Database $DB_NAME already exists."
fi

# Generate a .env file with dummy values
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating .env file with dummy values..."
    cat <<EOT > $ENV_FILE
ENV_STATE=dev

DEV_ADMIN_EMAIL=dummy_DEV_ADMIN_EMAIL
DEV_ADMIN_EMAIL_TOKEN=dummy_DEV_ADMIN_EMAIL_TOKEN

PROD_ADMIN_EMAIL=dummy_PROD_ADMIN_EMAIL
PROD_ADMIN_EMAIL_TOKEN=dummy_PROD_ADMIN_EMAIL_TOKEN
PROD_ADMIN_PASSWORD=dummy_PROD_ADMIN_PASSWORD
PROD_DB_URL=dummy_PROD_DB_URL
EOT
else
    echo ".env file already exists. Skipping creation."
fi

# Deactivate virtual environment
deactivate

echo "Setup complete. Virtual environment, dependencies, database, and .env file are ready."
