# setup_scheduler_task.ps1
# This script registers the Sensex stock market updater to run daily at 3:33 PM in the background.

# Get the directory of the current script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrEmpty($scriptDir)) {
    $scriptDir = Get-Location
}

$pythonPath = Join-Path $scriptDir "venv\Scripts\python.exe"
$appPath = Join-Path $scriptDir "app.py"

Write-Host "Registering Sensex Daily Update Task in Windows Task Scheduler..." -ForegroundColor Cyan
Write-Host "Project Directory: $scriptDir"
Write-Host "Python Path: $pythonPath"

# Validate paths
if (-not (Test-Path $pythonPath)) {
    Write-Host "Error: Virtual environment Python interpreter not found at $pythonPath." -ForegroundColor Red
    Write-Host "Please ensure you have created the virtual environment and installed requirements." -ForegroundColor Yellow
    exit 1
}

# Create Scheduled Task Action
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "app.py --run-once" -WorkingDirectory $scriptDir

# Create Trigger (Daily at 3:33 PM)
$trigger = New-ScheduledTaskTrigger -Daily -At "3:33PM"

# Create Settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register Scheduled Task
$taskName = "SensexDailyUpdate"
try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force
    Write-Host "Successfully registered scheduled task '$taskName' to run daily at 3:33 PM." -ForegroundColor Green
    Write-Host "The task will run in the background silently. You do not need to keep any command windows open!" -ForegroundColor Green
} catch {
    Write-Host "Failed to register scheduled task: $_" -ForegroundColor Red
    Write-Host "Try running this PowerShell script as Administrator." -ForegroundColor Yellow
}
