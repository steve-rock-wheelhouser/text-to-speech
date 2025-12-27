param(
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage
)

$Branch = "windows-mac"
$RemoteName = "origin"
$RemoteUrl = "https://github.com/steve-rock-wheelhouser/text-to-speech.git"
$GitPath = "C:\Program Files\Git\bin\git.exe"

# Check if branch exists locally
if (Test-Path ".git/refs/heads/$Branch") {
    Write-Host "Branch '$Branch' already exists locally. Switching to it."
    & $GitPath checkout $Branch
} else {
    Write-Host "Creating new branch '$Branch'."
    & $GitPath checkout -b $Branch
}

# Stage and commit changes
& $GitPath add .

if (& $GitPath diff --cached --quiet) {
    Write-Host "No changes to commit. Creating empty commit."
    & $GitPath commit --allow-empty -m $CommitMessage
} else {
    & $GitPath commit -m $CommitMessage
}

# Ensure remote is set
if (!(Test-Path ".git/refs/remotes/$RemoteName")) {
    Write-Host "Adding remote '$RemoteName' -> $RemoteUrl"
    & $GitPath remote add $RemoteName $RemoteUrl
}

# Push the branch
& $GitPath push -u $RemoteName $Branch

Write-Host "Successfully pushed to branch '$Branch' on GitHub."