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
  $markterm = "$HOME/source/repos/markterm"
  # Resolve script location:
  # Option A: put show_rendered_markdown.py somewhere stable and set this to that full path.
  # Option B: put it next to your profile and reference it from there.
  $program = "show_rendered_markdown.py"
  if (-not (Test-Path "$markterm/$program")) {
      throw "Could not find $program"
  }
}

process {
  $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop
  try {
    Push-Location $markterm

    .venv/Scripts/Activate.ps1

    # Skip theme for now, monokai code blocks look ugly
    #$args = @($program, $resolved.Path, "--theme", $Theme)
    $args = @($program, $resolved.Path)
    if ($PSBoundParameters.ContainsKey("Wrap")) {
      $args += @("--wrap", $Wrap)
    }

    & ".venv/Scripts/python.exe" @args
    & ".venv/Scripts/deactivate.bat"

  } finally {
    Pop-Location
  }
}
