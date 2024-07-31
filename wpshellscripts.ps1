########################################################
# MAIN Script with custom Windows Power Shell Functions
########################################################
$global:newjet = "C:\gitprojects\project_building_tools\create_project_structure.py"
$global:gitprojects = "C:\gitprojects"

$global:newjet = "C:\gitprojects\project_building_tools\create_project_structure@0.1.py"
$global:desktop = "C:\Users\mauricmm\iCloudDrive\#Desktop"
$global:gitprojects = "C:\gitprojects"
$uioadmin = "C:\Program Files\UiO Temporary Administrator\2.0.2\temp-admin-user.exe"
$exportenvs = "C:\gitprojects\project_building_tools\_scripts\export_envs.ps1"
$cloudgit = "C:\Users\mauricmm\iCloudDrive\cloudgit"


function touch {
    <#
    .SYNOPSIS
    Creates a new empty file or updates the timestamp of an existing file, with optional content.
    
    .EXAMPLE
    # Create a file named "test.txt" in the current directory
    touch -path "test.txt"
    
    # Create a file with specified content
    touch -path "C:\girprojects\test.txt" -content "This is the file content."
    #>
    param (
        [string]$path = "",
        [string]$content = ""
    )

    # If no path is provided, use the current directory
    if ($path -eq "") {
        $path = Join-Path -Path (Get-Location) -ChildPath "newfile.txt"
    }

    if (Test-Path $path) {
        # Error message if the file already exists
        Write-Error "File '$path' already exists."
    } else {
        # Create a new file with optional content
        New-Item -Path $path -ItemType File -Force | Out-Null
        if ($content -ne "") {
            Set-Content -Path $path -Value $content
        }
    }
}
