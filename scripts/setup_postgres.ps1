param(
    [string]$EnvPath = ".env",
    [string]$PostgresUser = "",
    [string]$PsqlPath = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

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
    }

    return $values
}

if (-not (Test-Path -LiteralPath $PsqlPath)) {
    throw "psql.exe was not found at $PsqlPath"
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
$DatabaseName = $envValues["POSTGRES_DB"]
$AppUser = $envValues["POSTGRES_USER"]
$AppPassword = $envValues["POSTGRES_PASSWORD"]
$PostgresHost = $envValues["POSTGRES_HOST"]
$PostgresPort = $envValues["POSTGRES_PORT"]
$AdminUser = if ($PostgresUser) { $PostgresUser } else { $AppUser }

if (-not $DatabaseName -or -not $AppUser -or -not $AppPassword) {
    throw ".env must define POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD"
}

if ($AdminUser -eq $AppUser) {
    $env:PGPASSWORD = $AppPassword
    Write-Host "Using POSTGRES_USER from .env for database initialization."
}
else {
    $adminPassword = Read-Host "Enter password for PostgreSQL user '$AdminUser'" -AsSecureString
    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($adminPassword)
    )
    $env:PGPASSWORD = $plainPassword

    Invoke-Native -FilePath $PsqlPath -Arguments @(
        "-h", $PostgresHost,
        "-p", $PostgresPort,
        "-U", $AdminUser,
        "-d", "postgres",
        "-v", "ON_ERROR_STOP=1",
        "-c", "DO `$`$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$AppUser') THEN CREATE ROLE $AppUser LOGIN PASSWORD '$AppPassword'; ELSE ALTER ROLE $AppUser WITH LOGIN PASSWORD '$AppPassword'; END IF; END `$`$;"
    )
}

$dbExists = & $PsqlPath -h $PostgresHost -p $PostgresPort -U $AdminUser -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$DatabaseName';"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to check whether database '$DatabaseName' exists."
}
$dbExistsValue = (@($dbExists) -join "").Trim()
if ($dbExistsValue -ne "1") {
    Invoke-Native -FilePath $PsqlPath -Arguments @(
        "-h", $PostgresHost,
        "-p", $PostgresPort,
        "-U", $AdminUser,
        "-d", "postgres",
        "-v", "ON_ERROR_STOP=1",
        "-c", "CREATE DATABASE $DatabaseName OWNER $AppUser;"
    )
}

Invoke-Native -FilePath $PsqlPath -Arguments @(
    "-h", $PostgresHost,
    "-p", $PostgresPort,
    "-U", $AdminUser,
    "-d", "postgres",
    "-v", "ON_ERROR_STOP=1",
    "-c", "GRANT ALL PRIVILEGES ON DATABASE $DatabaseName TO $AppUser;"
)

Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
Write-Host "PostgreSQL database '$DatabaseName' and user '$AppUser' are ready."
