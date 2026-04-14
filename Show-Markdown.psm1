function Show-Markdown {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory=$true, Position=0, ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$true)]
    [Alias("FullName")]
    [string] $Path,

    [Parameter(Mandatory=$false)]
    [int] $Wrap,

    [Parameter(Mandatory=$false)]
    [string] $Theme = "monokai",

    [Parameter(Mandatory=$false)]
    [Alias("Html")]
    [switch] $Browser
  )

  begin {
    $markterm = Get-Command markterm -ErrorAction SilentlyContinue
    if (-not $markterm) {
      $python = Get-Command py -ErrorAction SilentlyContinue
      if (-not $python) {
        $python = Get-Command python -ErrorAction SilentlyContinue
      }
      if (-not $python) {
        throw "Could not find 'markterm' or a Python launcher on PATH. Install markterm or activate the environment first."
      }
    }
  }

  process {
    $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop
    $args = @($resolved.Path, "--theme", $Theme)
    if ($PSBoundParameters.ContainsKey("Wrap")) {
      $args += @("--wrap", $Wrap)
    }
    if ($Browser) {
      $args += @("--browser")
    }

    if ($markterm) {
      & $markterm.Source @args
      return
    }

    & $python.Source -m markterm @args
  }
}

New-Alias -Name Render-Markdown -Value Show-Markdown

Export-ModuleMember -Function Show-Markdown
Export-ModuleMember -Alias Render-Markdown
