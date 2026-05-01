param(
    [switch]$SkipDbInit,
    [switch]$RunServer,
    [string]$EnvPath = ".env",
    [string]$PostgresAdminUser = "",
    [string]$PsqlPath = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

function Read-DotEnv {
    param([string]$Path)

    $values = @{}
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Environment file was not found at $Path"
    }

    Get-Content -LiteralPath $Path | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
            return
        }

        $parts = $line.Split("=", 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"').Trim("'")
        $values[$key] = $value
        Set-Item -Path "Env:$key" -Value $value
    }

    return $values
}

function Invoke-Step {
    param(
        [string]$Name,
        [scriptblock]$Command
    )

    Write-Host ""
    Write-Host "==> $Name" -ForegroundColor Cyan
    & $Command
}

function Invoke-Native {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $FilePath $($Arguments -join ' ')"
    }
}

$envValues = Read-DotEnv -Path $EnvPath
$pythonPath = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "Virtual environment Python was not found at $pythonPath"
}

Invoke-Step "Check Python and Django" {
    Invoke-Native -FilePath $pythonPath -Arguments @("--version")
    Invoke-Native -FilePath $pythonPath -Arguments @("-m", "django", "--version")
}

if (-not $SkipDbInit) {
    Invoke-Step "Create or update PostgreSQL database/user from .env" {
        & (Join-Path $PSScriptRoot "setup_postgres.ps1") -EnvPath $EnvPath -PostgresUser $PostgresAdminUser -PsqlPath $PsqlPath
    }
}

Invoke-Step "Verify Django configuration" {
    Invoke-Native -FilePath $pythonPath -Arguments @("manage.py", "check")
}

Invoke-Step "Run database migrations" {
    Invoke-Native -FilePath $pythonPath -Arguments @("manage.py", "migrate")
}

Invoke-Step "Verify PostgreSQL connection as app user" {
    $env:PGPASSWORD = $envValues["POSTGRES_PASSWORD"]
    Invoke-Native -FilePath $PsqlPath -Arguments @(
        "-h", $envValues["POSTGRES_HOST"],
        "-p", $envValues["POSTGRES_PORT"],
        "-U", $envValues["POSTGRES_USER"],
        "-d", $envValues["POSTGRES_DB"],
        "-c", "SELECT current_database(), current_user;"
    )
    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "AerUla development setup is ready." -ForegroundColor Green

if ($RunServer) {
    Invoke-Step "Start Django development server" {
        Invoke-Native -FilePath $pythonPath -Arguments @("manage.py", "runserver")
    }
}
else {
    Write-Host "Start the server with: .\.venv\Scripts\python.exe manage.py runserver"
}
