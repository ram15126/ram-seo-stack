# SEO System installer
#
#   .\install.ps1                      # link the skill + install Python deps
#   .\install.ps1 -RetireSuperseded    # also move superseded skills to _retired
#   .\install.ps1 -Uninstall           # remove the link, restore retired skills
#
# Nothing is deleted. Retired skills are moved to ~\.claude\skills\_retired\
# and can be restored at any time.

[CmdletBinding()]
param(
    [switch]$RetireSuperseded,
    [switch]$SkipDeps,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$repo      = $PSScriptRoot
$skillsDir = Join-Path $env:USERPROFILE '.claude\skills'
$retired   = Join-Path $skillsDir '_retired'

# Both skills ship from this repo. `seo` owns the site; `blog` owns the content
# published on it. `blog` reads scripts and references out of skills\seo, so the
# two are installed together and are not independently useful.
$skillNames = @('seo', 'blog')

# Kept for the uninstall path and the messages below.
$target    = Join-Path $skillsDir 'seo'
$source    = Join-Path $repo 'skills\seo'

# Superseded by this system: knowledge-only skills whose job a playbook now covers.
# Deliberately NOT listed: keyword-research, backlink-audit, semrush-research,
# ahrefs-research, search-console, google-analytics, similarweb-traffic,
# brand-monitor, aso, blog-writer. Those pull live data or hold personal
# config this system does not replace.
$superseded = @(
    'seo-audit', 'ai-seo', 'schema', 'programmatic-seo', 'site-architecture',
    'content-gap-analysis', 'seo-content-brief', 'serp-analyzer', 'competitors',
    'content-audit', 'geo-query-finder'
)

if ($Uninstall) {
    foreach ($name in $skillNames) {
        $p = Join-Path $skillsDir $name
        if (Test-Path $p) {
            Remove-Item $p -Recurse -Force -Confirm:$false
            Write-Host "Removed $p"
        }
    }
    if (Test-Path $retired) {
        Get-ChildItem $retired -Directory | ForEach-Object {
            Move-Item $_.FullName (Join-Path $skillsDir $_.Name)
            Write-Host "Restored $($_.Name)"
        }
        Remove-Item $retired -Force -ErrorAction SilentlyContinue
    }
    Write-Host "`nUninstalled. Restart Claude Code to pick up the change." -ForegroundColor Green
    return
}

if (-not (Test-Path $skillsDir)) { New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null }

# --- 1. Link the skills ------------------------------------------------------
$copiedAny = $false
foreach ($name in $skillNames) {
    $src = Join-Path $repo "skills\$name"
    $dst = Join-Path $skillsDir $name
    if (-not (Test-Path $src)) { throw "Cannot find $src. Run this from the repo root." }
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force -Confirm:$false }
    try {
        New-Item -ItemType SymbolicLink -Path $dst -Target $src -ErrorAction Stop | Out-Null
        Write-Host "Linked  $dst -> $src" -ForegroundColor Green
    } catch {
        # Symlinks need Developer Mode or admin on Windows; copying is the fallback.
        Copy-Item $src $dst -Recurse -Force
        $copiedAny = $true
        Write-Host "Copied  $src -> $dst" -ForegroundColor Yellow
    }
}
if ($copiedAny) {
    Write-Host "        (symlink unavailable; re-run install.ps1 after editing the repo)" -ForegroundColor DarkYellow
    Write-Host "        NOTE: copies drift. If you edit a reference or script in the repo," -ForegroundColor DarkYellow
    Write-Host "        the installed copy keeps the old text until you re-run this." -ForegroundColor DarkYellow
}

# --- 2. Python dependencies --------------------------------------------------
if (-not $SkipDeps) {
    Write-Host "`nInstalling Python dependencies (requests, beautifulsoup4, lxml)..."
    try {
        python -m pip install --user --quiet --disable-pip-version-check requests beautifulsoup4 lxml
        python -c "import requests, bs4, lxml" 2>$null
        if ($?) { Write-Host "Python deps OK" -ForegroundColor Green }
    } catch {
        Write-Host "Could not install deps automatically. Run manually:" -ForegroundColor Yellow
        Write-Host "  python -m pip install --user requests beautifulsoup4 lxml"
    }
    Write-Host "Optional (screenshots / mobile render checks): python -m pip install --user playwright; playwright install chromium" -ForegroundColor DarkGray
}

# --- 3. Retire superseded skills --------------------------------------------
if ($RetireSuperseded) {
    if (-not (Test-Path $retired)) { New-Item -ItemType Directory -Path $retired -Force | Out-Null }
    $moved = 0
    foreach ($name in $superseded) {
        $p = Join-Path $skillsDir $name
        if (Test-Path $p) {
            Move-Item $p (Join-Path $retired $name) -Force
            Write-Host "Retired $name"
            $moved++
        }
    }
    Write-Host "Retired $moved skill(s) to $retired (restore with -Uninstall)" -ForegroundColor Green
} else {
    Write-Host "`nSuperseded skills left in place. To retire them:" -ForegroundColor DarkGray
    Write-Host "  .\install.ps1 -RetireSuperseded" -ForegroundColor DarkGray
}

Write-Host "`nDone. Restart Claude Code, then try:" -ForegroundColor Green
Write-Host "  seo audit https://<a-client-site>" -ForegroundColor Green
Write-Host "  blog audit https://<a-client-site>/blog/<a-post>" -ForegroundColor Green
