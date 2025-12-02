# PowerShell script to run the chatbot
# Usage: .\run.ps1 [--console|--test|--api]

param(
    [string]$Mode = "api"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Drone FAQ Chatbot Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python availability
try {
    $pythonVersion = py --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python or use 'py' command." -ForegroundColor Red
    exit 1
}

# Run based on mode
switch ($Mode.ToLower()) {
    "console" {
        Write-Host "Starting Console Mode..." -ForegroundColor Yellow
        Write-Host ""
        py app.py --console
    }
    "test" {
        Write-Host "Running Tests..." -ForegroundColor Yellow
        Write-Host ""
        py app.py --test
    }
    "api" {
        Write-Host "Starting API Server..." -ForegroundColor Yellow
        Write-Host ""
        py app.py
    }
    default {
        Write-Host "Invalid mode. Use: console, test, or api" -ForegroundColor Red
        Write-Host "Example: .\run.ps1 --console" -ForegroundColor Yellow
    }
}

