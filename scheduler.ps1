# Set the working directory to the script's location
Set-Location -Path $PSScriptRoot

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Log the start of the application
Write-Output "Starting YOLO RTSP Python application at $(Get-Date)"

# Start the Python application and wait for it to exit
$process = Start-Process -FilePath "python" -ArgumentList "main.py --stream rtsp://yolo-stream:yolo43026@192.168.2.185/Preview_01_main --yolo person" -PassThru -WorkingDirectory $PSScriptRoot -WindowStyle Hidden
$process | Wait-Process

# Log the exit code
Write-Output "Python application exited with code $($process.ExitCode) at $(Get-Date)"
