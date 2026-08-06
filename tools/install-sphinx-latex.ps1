#requires -version 5
<#
.SYNOPSIS
  Make Sphinx's LaTeX class visible to TinyTeX, so `--profile sphinx --to sphinxdoc-pdf`
  can render.

.DESCRIPTION
  sphinxmanual.cls is NOT on CTAN -- verified, `tlmgr search --global --file
  sphinxmanual.cls` returns nothing -- so it cannot be installed the way ieeetran
  was. Sphinx ships it inside the Python package instead, in sphinx/texinputs/.

  This copies the .cls/.sty set into the local TeX tree and reindexes. It is the
  one manual setup step the Sphinx format needs; everything else about that
  format is in the repository.

  Run once per machine. Re-running is harmless and picks up a newer Sphinx.

  Files are BSD-licensed and copied rather than symlinked, so the format keeps
  working if the Python sphinx package is later removed or upgraded.

  NOTHING HERE IS HARDCODED TO ONE MACHINE. The TeX tree is discovered by asking
  kpsewhich for TEXMFLOCAL, and the interpreter is chosen by testing candidates
  for an importable sphinx. Both are still overridable by parameter when the
  guess is wrong.

.PARAMETER Python
  Interpreter to source the files from. Omit to auto-detect the first candidate
  that can import sphinx.

.PARAMETER TexmfLocal
  Destination directory. Omit to derive it from kpsewhich's TEXMFLOCAL.

.EXAMPLE
  .\tools\install-sphinx-latex.ps1
.EXAMPLE
  .\tools\install-sphinx-latex.ps1 -Python C:\path\to\python.exe
#>
[CmdletBinding()]
param(
  [string]$Python,
  [string]$TexmfLocal
)

$ErrorActionPreference = 'Stop'

# --- 1. Locate kpsewhich -----------------------------------------------------
# Everything else about the TeX side is derived from it: mktexlsr is its
# neighbour, and TEXMFLOCAL is something it will simply tell us. TinyTeX installs
# per-user or system-wide depending on how it was set up, and Quarto's own copy
# is elsewhere again -- so search rather than assume. The bin/*/ glob also covers
# non-Windows layouts (bin/x86_64-darwin, bin/x86_64-linux) at no extra cost.
$kpsewhich = (Get-Command kpsewhich -ErrorAction SilentlyContinue).Source

if (-not $kpsewhich) {
  $roots = @(
    "$env:APPDATA\TinyTeX"
    "$env:LOCALAPPDATA\TinyTeX"
    "$env:ProgramData\TinyTeX"
    "$env:USERPROFILE\.TinyTeX"
    "$env:LOCALAPPDATA\Programs\quarto\bin\tools"
    "$HOME/.TinyTeX"
    "/usr/local/texlive"
  ) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }

  foreach ($root in $roots) {
    $hit = Get-ChildItem -Path $root -Filter 'kpsewhich*' -Recurse -File -ErrorAction SilentlyContinue |
           Where-Object { $_.Extension -in '.exe', '' } |
           Select-Object -First 1
    if ($hit) { $kpsewhich = $hit.FullName; break }
  }
}

if (-not $kpsewhich) {
  throw @'
kpsewhich not found. Install a TeX distribution first:

    quarto install tinytex

If TeX is installed somewhere unusual, put its bin directory on PATH and re-run.
'@
}

$texBin   = Split-Path -Parent $kpsewhich
$mktexlsr = Get-ChildItem -Path $texBin -Filter 'mktexlsr*' -File -ErrorAction SilentlyContinue |
            Select-Object -First 1
if (-not $mktexlsr) { throw "mktexlsr not found beside kpsewhich in $texBin." }

Write-Host ("  tex tools: {0}" -f $texBin)

# --- 2. Resolve the destination ----------------------------------------------
# kpsewhich knows TEXMFLOCAL; hardcoding it breaks on every other install layout.
if (-not $TexmfLocal) {
  $texmfRoot = (& $kpsewhich -var-value=TEXMFLOCAL 2>$null | Select-Object -First 1)
  if (-not $texmfRoot) { throw "kpsewhich could not report TEXMFLOCAL. Pass -TexmfLocal explicitly." }
  $TexmfLocal = Join-Path ($texmfRoot -replace '/', [IO.Path]::DirectorySeparatorChar) 'tex/latex/sphinx'
}
Write-Host ("  destination: {0}" -f $TexmfLocal)

# --- 3. Find an interpreter that actually has sphinx -------------------------
# Testing the import is the only reliable check: a machine can carry several
# interpreters where only one has sphinx, and the bare `python` on PATH is often
# not that one.
function Test-HasSphinx([string]$exe) {
  try {
    $v = & $exe -c "import sphinx; print(sphinx.__version__)" 2>$null
    if ($LASTEXITCODE -eq 0 -and $v) { return $v.Trim() }
  } catch { }
  return $null
}

$candidates = @()
if ($Python) { $candidates += $Python }
$candidates += @('python', 'python3', 'py')

$pythonExe = $null; $sphinxVersion = $null
foreach ($c in $candidates) {
  if ($c -eq 'py') {
    # The Windows launcher needs a version selector before -c.
    try {
      $v = & py -3 -c "import sphinx; print(sphinx.__version__)" 2>$null
      if ($LASTEXITCODE -eq 0 -and $v) { $pythonExe = 'py'; $sphinxVersion = $v.Trim(); break }
    } catch { }
    continue
  }
  if (-not $Python -and -not (Get-Command $c -ErrorAction SilentlyContinue)) { continue }
  $v = Test-HasSphinx $c
  if ($v) { $pythonExe = $c; $sphinxVersion = $v; break }
}

if (-not $pythonExe) {
  throw @'
No interpreter with sphinx was found. Install it into one of them, then re-run:

    python -m pip install sphinx

If sphinx lives in an interpreter not on PATH (a conda env, a venv), point at it:

    .\tools\install-sphinx-latex.ps1 -Python C:\path\to\python.exe

Only this setup step needs sphinx. Once the class files are copied, rendering
does not use it -- the format is a Quarto extension, not a Sphinx build.
'@
}

$pyArgs = @(); if ($pythonExe -eq 'py') { $pyArgs = @('-3') }
Write-Host ("  interpreter: {0} (sphinx {1})" -f $pythonExe, $sphinxVersion)

# --- 4. Copy the class/style set ---------------------------------------------
# Ask Sphinx where its own texinputs live rather than hardcoding a site-packages
# path -- that path changes with every Python minor version and with venvs.
$texinputs = & $pythonExe @pyArgs -c "import sphinx,pathlib;print(pathlib.Path(sphinx.__file__).parent/'texinputs')"
if (-not (Test-Path -LiteralPath $texinputs)) {
  throw "Sphinx texinputs not found at $texinputs."
}

New-Item -ItemType Directory -Force -Path $TexmfLocal | Out-Null
$files = Get-ChildItem -LiteralPath $texinputs -File |
         Where-Object { $_.Extension -in '.cls', '.sty' }
foreach ($f in $files) {
  Copy-Item -LiteralPath $f.FullName -Destination $TexmfLocal -Force
}
Write-Host ("  copied {0} class/style file(s)" -f $files.Count)

# --- 5. Generate sphinxhighlight.sty -----------------------------------------
# It is NOT in texinputs. Sphinx generates it per project from the chosen
# Pygments theme, and sphinx.sty does \RequirePackage{sphinxhighlight}
# unconditionally -- so without this the render dies on a missing file that no
# amount of copying texinputs will supply. Generated once here with the default
# theme, which is what the Python manual itself uses.
$genHighlight = @'
import sys, pathlib
from sphinx.highlighting import PygmentsBridge
out = pathlib.Path(sys.argv[1]) / "sphinxhighlight.sty"
out.write_text(PygmentsBridge("latex", "default").get_stylesheet(), encoding="utf-8")
print(out)
'@
$tmpPy = Join-Path ([IO.Path]::GetTempPath()) 'gen_sphinxhighlight.py'
Set-Content -LiteralPath $tmpPy -Value $genHighlight -Encoding UTF8
& $pythonExe @pyArgs $tmpPy $TexmfLocal
Remove-Item -LiteralPath $tmpPy -Force

# --- 6. Reindex and verify ---------------------------------------------------
# Without this the files are on disk but invisible: kpathsea reads ls-R, not the
# directory, so the render still fails with "File `sphinxmanual.cls' not found".
& $mktexlsr.FullName 2>&1 | Select-Object -Last 1

$found = & $kpsewhich 'sphinxmanual.cls'
if (-not $found) { throw "sphinxmanual.cls still not resolvable after mktexlsr." }
Write-Host "  OK: $found"

$foundHl = & $kpsewhich 'sphinxhighlight.sty'
if (-not $foundHl) { throw "sphinxhighlight.sty still not resolvable after mktexlsr." }
Write-Host "  OK: $foundHl"
