########################################################
# MAIN Script with custom Windows Power Shell Functions
########################################################
$global:newjet = "C:\gitprojects\project_building_tools\create_project_structure@0.1.py"
$monitordir = "C:\gitprojects\project_building_tools\monitor_log_txt_changes@0.1.py"

$global:desktop = "C:\Users\mauricmm\cloud\iCloudDrive\#Desktop"
$global:gitprojects = "C:\gitprojects"
$uioadmin = "C:\Program Files\UiO Temporary Administrator\2.0.2\temp-admin-user.exe"
$exportenvs = "C:\gitprojects\project_building_tools\_scripts\export_envs.ps1"
$cbatchinstall = "C:\gitprojects\project_building_tools\_scripts\conda batch_install.ps1"
$cloudgit = "C:\Users\mauricmm\iCloudDrive\cloudgit"
$uiodropbox = "C:\Users\mauricmm\UiO Dropbox\Mauricio Mandujano Manriquez"
$pandoc = "C:\gitprojects\project_building_tools\_format_converters"
$pandocpdf = "C:\gitprojects\project_building_tools\_format_converters\paper_convert.py"


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
function Add-EscapeBacktick {
    <#
    .SYNOPSIS
        Adds escape backticks to `[` and `]` characters in a given file path.

    .DESCRIPTION
        The Add-EscapeBacktick function takes a file path as input and returns the file path with escape backticks 
        added before each `[` and `]` character. This is useful for handling file paths with special characters 
        in PowerShell scripts.

    .PARAMETER FilePath
        The file path to be processed.

    .EXAMPLE
        $filePath = "C:\Program Files\Example[Path]\Folder]"
        $escapedFilePath = Add-EscapeBacktick -FilePath $filePath
        Write-Output $escapedFilePath
        # Output: C:\Program Files\Example`[Path`]\Folder`]

    .NOTES
        This function uses the `-replace` operator to perform the character replacement.
    #>
    param (
        [string]$FilePath
    )

    # Replace each occurrence of [ with `[ and ] with `]
    $EscapedFilePath = $FilePath -replace '\[', '``\[' -replace '\]', '``\]'

    return $EscapedFilePath
}
