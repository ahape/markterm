[CmdletBinding()]
param(
  [Parameter(Mandatory=$true, Position=0, ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$true)]
  [Alias("FullName")]
  [string] $Path,

  [Parameter(Mandatory=$false)]
  [int] $Wrap,

  [Parameter(Mandatory=$false)]
  [string] $Theme = "monokai"
)


begin {
  # Use $PSScriptRoot to locate the script directory dynamically
  $markterm = $PSScriptRoot

  # Use the new package structure
  $program = "markterm\cli.py"

  # Check if running from repository (has cli.py)
  if (Test-Path "$markterm/$program") {
    $useLocalScript = $true
  }
  # Otherwise, try to use installed package
  elseif (Get-Command markterm -ErrorAction SilentlyContinue) {
    $useLocalScript = $false
  }
  else {
    throw "Could not find markterm. Either run from repository or install with: pip install -e ."
  }
}

process {
  $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop

  if ($useLocalScript) {
    # Use local development version
    try {
      Push-Location $markterm

      # Activate virtual environment if it exists
      if (Test-Path ".venv/Scripts/Activate.ps1") {
        .venv/Scripts/Activate.ps1
      }

      # Build arguments
      $args = @($program, $resolved.Path, "--theme", $Theme)
      if ($PSBoundParameters.ContainsKey("Wrap")) {
        $args += @("--wrap", $Wrap)
      }

      & ".venv/Scripts/python.exe" @args

      # Deactivate if deactivate.bat exists
      if (Test-Path ".venv/Scripts/deactivate.bat") {
        & ".venv/Scripts/deactivate.bat"
      }

    } finally {
      Pop-Location
    }
  }
  else {
    # Use installed package
    $args = @($resolved.Path, "--theme", $Theme)
    if ($PSBoundParameters.ContainsKey("Wrap")) {
      $args += @("--wrap", $Wrap)
    }

    & markterm @args
  }
}
