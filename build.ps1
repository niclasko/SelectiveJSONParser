# Update version in pyproject.toml and src/selectivejsonparser/__init__.py

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("patch", "minor", "major")]
    [string]$VersionType = "patch",
    
    [Parameter(Mandatory=$false)]
    [switch]$Release
)

function Get-CurrentVersion {
    $pyprojectContent = Get-Content -Path "pyproject.toml" -Raw
    
    # Extract version using regex
    if ($pyprojectContent -match 'version\s*=\s*"([^"]+)"') {
        return $matches[1]
    }
    
    throw "Could not find version in pyproject.toml"
}

function Increment-Version {
    param(
        [string]$Version,
        [string]$Type
    )
    
    # Parse semantic version (major.minor.patch)
    if ($Version -match '^(\d+)\.(\d+)\.(\d+)$') {
        $major = [int]$matches[1]
        $minor = [int]$matches[2] 
        $patch = [int]$matches[3]
        
        switch ($Type) {
            "major" { 
                $major++
                $minor = 0
                $patch = 0
            }
            "minor" { 
                $minor++
                $patch = 0
            }
            "patch" { 
                $patch++
            }
        }
        
        return "$major.$minor.$patch"
    }
    
    throw "Invalid version format: $Version. Expected format: major.minor.patch"
}

function Update-PyprojectVersion {
    param([string]$NewVersion)
    
    $content = Get-Content -Path "pyproject.toml" -Raw
    $updatedContent = $content -replace 'version\s*=\s*"[^"]+"', "version = `"$NewVersion`""
    Set-Content -Path "pyproject.toml" -Value $updatedContent -NoNewline
    
    Write-Host "Updated pyproject.toml version to: $NewVersion" -ForegroundColor Green
}

function Update-InitPyVersion {
    param([string]$NewVersion)
    
    $initPath = "src\selectivejsonparser\__init__.py"
    $content = Get-Content -Path $initPath -Raw
    $updatedContent = $content -replace '__version__\s*=\s*"[^"]+"', "__version__ = `"$NewVersion`""
    Set-Content -Path $initPath -Value $updatedContent -NoNewline
    
    Write-Host "Updated $initPath version to: $NewVersion" -ForegroundColor Green
}

function Push-Changes {
    param([string]$Message)
    
    git add pyproject.toml src/selectivejsonparser/__init__.py
    git commit -m $Message
    git push origin main
    Write-Host "Pushed changes to git with message: $Message" -ForegroundColor Green
}

# Main script execution
try {
    Write-Host "Building SelectiveJSONParser..." -ForegroundColor Cyan
    
    # Get current version
    $currentVersion = Get-CurrentVersion
    Write-Host "Current version: $currentVersion" -ForegroundColor Yellow
    
    # Increment version
    $newVersion = Increment-Version -Version $currentVersion -Type $VersionType
    Write-Host "New version: $newVersion" -ForegroundColor Yellow
    
    # Update both files
    Update-PyprojectVersion -NewVersion $newVersion
    Update-InitPyVersion -NewVersion $newVersion

    # Commit and push changes
    Push-Changes -Message "Bump version to $newVersion"
    
    Write-Host "`nVersion update completed successfully!" -ForegroundColor Green
    Write-Host "Updated from $currentVersion to $newVersion ($VersionType increment)" -ForegroundColor Green
    
} catch {
    Write-Error "Build failed: $($_.Exception.Message)"
    exit 1
}

# Run tests to verify everything is working
try {
    Write-Host "Running tests..." -ForegroundColor Cyan
    python -m pytest tests/
    Write-Host "All tests passed!" -ForegroundColor Green
} catch {
    Write-Error "Tests failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Build the package
Write-Host "Building the package..." -ForegroundColor Cyan
try {
    # Delete previous builds
    if (Test-Path -Path "dist") {
        Remove-Item -Path "dist" -Recurse -Force
        Write-Host "Deleted previous builds in 'dist/'" -ForegroundColor Yellow
    }
    # Ensure build module is installed
    if (-not (Get-Command "python -m build" -ErrorAction SilentlyContinue)) {
        Write-Host "Build module not found. Installing build module..." -ForegroundColor Yellow
        try {
            python -m pip install --upgrade build
        } catch {
            throw "Failed to install build module. Please install it manually and try again."
        }
    }
    python -m build
    Write-Host "Package built successfully!" -ForegroundColor Green
} catch {
    Write-Error "Package build failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Tag the new version in git
try {
    git tag "v$newVersion"
    git push origin "v$newVersion"
    Write-Host "Tagged the new version in git: v$newVersion" -ForegroundColor Green
} catch {
    Write-Error "Git tagging failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Release to PyPI
if ($Release) {
    Write-Host "Releasing to PyPI..." -ForegroundColor Cyan
    try {
        # Check that twine is installed
        if (-not (Get-Command "python -m twine" -ErrorAction SilentlyContinue)) {
            Write-Host "Twine not found. Installing twine..." -ForegroundColor Yellow
            try {
                python -m pip install --upgrade twine
            } catch {
                throw "Failed to install twine. Please install it manually and try again."
            }
        }
        python -m twine check dist/*
        python -m twine upload --repository testpypi dist/*
        python -m twine upload dist/*
        Write-Host "Released to PyPI successfully!" -ForegroundColor Green
    } catch {
        Write-Error "Release to PyPI failed: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Skipping release to PyPI. Use --release flag to enable." -ForegroundColor Yellow
}