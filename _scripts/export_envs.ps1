# Set variables
$envDetails = @(
    @{ Name = "base"; Path = "C:\Users\mauricmm\Anaconda3" },
    @{ Name = "scifipy"; Path = "C:\Users\mauricmm\Anaconda3\envs\scifipy" }
)
$gitRepoPath = "C:\gitprojects\project_building_tools\_envs"
$commitMessage = "Update Conda environments - $(Get-Date -Format 'yyyy-MM-dd')"

# Activate conda
Write-Output "Activating Conda environment..."
& "C:\Users\mauricmm\Anaconda3\shell\condabin\conda-hook.ps1"

foreach ($env in $envDetails) {
    $envName = $env.Name
    $yamlFileName = "$envName-environment.yml"

    # Activate the conda environment
    Write-Output "Activating Conda environment: $envName"
    conda activate $envName

    # Export the conda environment directly to the Git repository path
    Write-Output "Exporting Conda environment to $gitRepoPath\$yamlFileName"
    conda env export > "$gitRepoPath\$yamlFileName"
}

# Change to the Git repository directory
Write-Output "Changing to Git repository directory: $gitRepoPath"
Set-Location -Path $gitRepoPath

# Add the changes to Git
Write-Output "Adding changes to Git repository..."
git add *.yml

# Commit the changes
Write-Output "Committing changes to Git repository..."
git commit -m $commitMessage

# Push changes to the remote repository
Write-Output "Pushing changes to remote Git repository..."
git push

# Deactivate conda environment
Write-Output "Deactivating Conda environment..."
conda deactivate

Write-Output "Script execution completed."
