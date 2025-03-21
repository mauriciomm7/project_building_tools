# Set variables
$envDetails = @(
    @{ Name = "base"; Path = "C:\Users\mauricmm\Anaconda3" },
    @{ Name = "scifipy"; Path = "C:\Users\mauricmm\Anaconda3\envs\scifipy" },
    @{ Name = "dataviz"; Path = "C:\Users\mauricmm\Anaconda3\envs\dataviz" },
    @{ Name = "llm"; Path = "C:\Users\mauricmm\Anaconda3\envs\llm" },
    @{ Name = "blacksmith"; Path = "C:\Users\mauricmm\Anaconda3\envs\blacksmith" },
    @{ Name = "condarstudio"; Path = "C:\Users\mauricmm\Anaconda3\envs\condarstudio" },
    @{ Name = "mathviz"; Path = "C:\Users\mauricmm\Anaconda3\envs\mathviz" }

)
$gitRepoPath = "C:\gitprojects\project_building_tools\_envs"
$commitMessage = "Update Conda environments - $(Get-Date -Format 'yyyy-MM-dd')"

# SAVE current working directory  dir
$originaldir = Get-Location

# Activate conda
Write-Output "Activating Conda environment..."
& "C:\Users\mauricmm\Anaconda3\shell\condabin\conda-hook.ps1"

foreach ($env in $envDetails) {
    $envName = $env.Name
    $yamlFileName = "$envName-environment.yml"

    # Activate the conda environment
    Write-Host "Activating Conda environment: $envName"
    conda activate $envName

    # Export the conda environment directly to the Git repository path
    Write-Host "Exporting Conda environment to $gitRepoPath\$yamlFileName"
    conda env export > "$gitRepoPath\$yamlFileName"
}

# Change to the Git repository directory
Write-Host "Changing to Git repository directory: $gitRepoPath"
Set-Location -Path $gitRepoPath

# Add the changes to Git
Write-Host "Adding changes to Git repository..."
git add *.yml

# Commit the changes
Write-Host "Committing changes to Git repository..."
git commit -m $commitMessage

# Push changes to the remote repository
Write-Host "Pushing changes to remote Git repository..."
git push

# Deactivate conda environment
Write-Host "Deactivating Conda environment..."
conda deactivate

Write-Host "Script execution completed."

# Change back to original dir 
Write-Host "All done! You are back here.:D"
Set-Location $originaldir
