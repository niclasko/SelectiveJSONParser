# SelectiveJSONParser Environment Setup Script
# 
# To run this script and have the environment activated in your current shell:
# 1. Run: & .\create_env.ps1
# 2. Then run: conda activate selectivejsonparser
#
# Or run each command manually from this script.

# Create environment with Python 3.11
Write-Host "Creating conda environment 'selectivejsonparser'..." -ForegroundColor Green
conda create -n selectivejsonparser python=3.10 -y

# Note: conda activate doesn't work properly in PowerShell scripts
# The environment will need to be activated manually after the script completes
Write-Host "Note: You'll need to activate the environment manually with 'conda activate selectivejsonparser'" -ForegroundColor Yellow

# Install pip and build tools
Write-Host "Installing pip..." -ForegroundColor Green
conda install pip -y

# Install using conda run to ensure proper environment context
Write-Host ""
$installDev = Read-Host "Install development dependencies (pytest, black, flake8, mypy)? [y/N]"

if ($installDev -eq "y" -or $installDev -eq "Y" -or $installDev -eq "yes") {
    Write-Host "Installing project in editable mode with dev dependencies..." -ForegroundColor Green
    conda run -n selectivejsonparser pip install -e ".[dev]"
} else {
    Write-Host "Installing project in editable mode..." -ForegroundColor Green
    conda run -n selectivejsonparser pip install -e .
}

Write-Host "" -ForegroundColor Green
Write-Host "Environment setup complete!" -ForegroundColor Green
Write-Host "To activate the environment, run: conda activate selectivejsonparser" -ForegroundColor Cyan
Write-Host "To run tests, use: python -m pytest tests/ -v" -ForegroundColor Cyan