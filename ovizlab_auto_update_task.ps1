# Windows Task Scheduler registration. Preview by default, explicit -Apply needed.
[CmdletBinding()]
param(
  [switch]$Enable,
  [switch]$Disable,
  [switch]$Apply,
  [string]$UpdaterScript,
  [string]$StatePath = "$env:LOCALAPPDATA\OVizLAB\auto-update\state.json",
  [string]$At = "10:00",
  [string]$TaskName = "OVizLAB-Skills-AutoUpdate"
)
$ErrorActionPreference = 'Stop'
if ([bool]$Enable -eq [bool]$Disable) { throw 'Choose exactly one: -Enable or -Disable' }
if ($TaskName -ne "OVizLAB-Skills-AutoUpdate") { throw 'Unexpected task name' }
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($Disable) {
  if (-not $existing) { Write-Output 'NO_TASK'; exit 0 }
  if (-not $Apply) { Write-Output "PREVIEW: disable task '$TaskName' (no changes)"; exit 0 }
  Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
  if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) { throw 'TASK_REMOVE_FAILED' }
  Write-Output 'TASK_REMOVED'
  exit 0
}
if ($existing) { throw 'TASK_ALREADY_EXISTS: inspect it manually; no replacement' }
if ([string]::IsNullOrWhiteSpace($UpdaterScript)) { throw 'UpdaterScript absolute path required' }
if (-not [IO.Path]::IsPathRooted($UpdaterScript)) { throw 'UpdaterScript must be an absolute path' }
$source = Get-Item -LiteralPath $UpdaterScript -ErrorAction Stop
if ($source.PSIsContainer -or ($source.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
  throw 'UNSAFE_UPDATER_SCRIPT'
}
if ($source.Name -ne 'auto_update.py' -and $source.Name -ne 'agent_auto_updater.py') {
  throw 'UNEXPECTED_UPDATER_SCRIPT'
}
if (-not [IO.Path]::IsPathRooted($StatePath) -or -not (Test-Path -LiteralPath $StatePath -PathType Leaf)) {
  throw 'ENROLLED_STATE_REQUIRED'
}
$stateItem = Get-Item -LiteralPath $StatePath
if ($stateItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'SYMLINKED_STATE_BLOCKED' }
try { $state = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json } catch { throw 'INVALID_STATE_JSON' }
if ($state.schema_version -ne 1 -or $state.repository -ne 'lutiy-dev/OVizLAB-Skills' -or $state.agent -ne 'codex') {
  throw 'STATE_IDENTITY_MISMATCH'
}
if ($At -notmatch '^(?:[01][0-9]|2[0-3]):[0-5][0-9]$') { throw 'INVALID_SCHEDULE_TIME' }
$python = Get-Command py.exe -ErrorAction SilentlyContinue
if (-not $python) { throw 'PYTHON_LAUNCHER_NOT_FOUND: install/verify Python 3.10+ first' }
$arguments = '-3 "' + $source.FullName + '" run --state "' + $stateItem.FullName + '"'
$summary = [ordered]@{
  status = $(if ($Apply) { 'READY_TO_REGISTER' } else { 'PREVIEW_ONLY' })
  task_name = $TaskName
  daily_local_time = $At
  executable = $python.Source
  args = $arguments
  enrolled_skills = @($state.installed.PSObject.Properties).Count
  run_as = "$env:USERDOMAIN\$env:USERNAME"
  write_scope = 'Only enrolled unchanged Codex Skills, with installer backup receipts'
}
$summary | ConvertTo-Json -Depth 4
if (-not $Apply) { exit 0 }
$parts = $At.Split(':')
$triggerAt = (Get-Date).Date.AddHours([int]$parts[0]).AddMinutes([int]$parts[1])
$action = New-ScheduledTaskAction -Execute $python.Source -Argument $arguments
$trigger = New-ScheduledTaskTrigger -Daily -At $triggerAt
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'OVizLAB opt-in guarded Skills updates' -ErrorAction Stop | Out-Null
if (-not (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue)) { throw 'TASK_REGISTER_VERIFY_FAILED' }
Write-Output 'TASK_REGISTERED'
