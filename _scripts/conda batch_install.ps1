# Usage: .\install_in_env.ps1 <package_name> [<version>]

# Check if the first parameter (package name) is provided
if ($args.Count -lt 1) {
    Write-Host "Usage: .\install_in_env.ps1 <package_name> [<version>]"
    exit 1
}

$packageName = $args[0]
$packageVersion = if ($args.Count -ge 2) { $args[1] } else { "latest" }  # Default to "latest" if no version is provided

# Function to install package in the given environment
function Install-Package {
    param (
        [string]$envName
    )

    Write-Host "Installing $packageName ($packageVersion) in $envName environment..."

    # Activate the environment
    conda activate $envName

    # Install the package (use pip if it's not available in conda)
    if ($packageVersion -eq "latest") {
        conda install $packageName -c conda-forge -y
        if ($LASTEXITCODE -ne 0) {
            pip install $packageName
        }
    } else {
        conda install "$packageName=$packageVersion" -c conda-forge -y
        if ($LASTEXITCODE -ne 0) {
            pip install "$packageName==$packageVersion"
        }
    }

    Write-Host "$packageName installed in $envName"
}

# Install the package in each environment
$environments = @("base", "llm", "blacksmith", "scifipy")
foreach ($env in $environments) {
    Install-Package -envName $env
}

# Deactivate the environment after installation
conda deactivate

Write-Host "Package installation completed in all environments."
