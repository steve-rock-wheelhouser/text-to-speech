# Setup Virtual Environment Script
# This script creates a virtual environment and installs requirements

# Set the paths
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $PSScriptRoot ".venv"
$RequirementsPath = Join-Path $ProjectRoot "requirements.txt"

# Create virtual environment if it doesn't exist
if (!(Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment..."
    python -m venv $VenvPath
} else {
    Write-Host "Virtual environment already exists."
}

# Set paths to venv executables
$PythonExe = Join-Path $VenvPath "Scripts\python.exe"
$PipExe = Join-Path $VenvPath "Scripts\pip.exe"

# Upgrade pip
Write-Host "Upgrading pip..."
& $PythonExe -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..."
# On Windows, skip patchelf which is Linux-only
$requirements = Get-Content $RequirementsPath | Where-Object { $_ -notmatch "^patchelf" -and $_ -ne "" }
foreach ($req in $requirements) {
    & $PipExe install $req
}

Write-Host "Virtual environment setup complete!"