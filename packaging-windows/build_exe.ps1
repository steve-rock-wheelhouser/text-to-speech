# Build Windows Executable Script
# This script builds the Windows executable using the existing virtual environment

# Set the paths
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $PSScriptRoot ".venv"
$MainScriptPath = Join-Path $ProjectRoot "src\text_to_speech.py"
$DistPath = Join-Path $PSScriptRoot "dist"

# Check if venv exists
if (!(Test-Path $VenvPath)) {
    Write-Host "Virtual environment not found. Please run setup_venv.ps1 first."
    exit 1
}

# Set paths to venv executables
#$PythonExe = Join-Path $VenvPath "Scripts\python.exe"

# Create dist directory if it doesn't exist
if (Test-Path $DistPath) {
    Remove-Item -Recurse -Force $DistPath
}
New-Item -ItemType Directory -Path $DistPath | Out-Null

# Build the executable using PyInstaller
Write-Host "Building Windows executable..."
$PyInstallerExe = Join-Path $VenvPath "Scripts\pyinstaller.exe"
$IconPath = Join-Path $ProjectRoot "assets\icons\icon.ico"
$VoicesPath = Join-Path $ProjectRoot "src\voices.json"
$AssetsPath = Join-Path $ProjectRoot "assets"
& $PyInstallerExe --onefile --windowed --icon $IconPath --name "Text to Speech" --add-data "$VoicesPath;." --add-data "$AssetsPath;assets" --distpath $DistPath --workpath (Join-Path $PSScriptRoot "build") $MainScriptPath

Write-Host "Build complete! Executable should be in $DistPath"