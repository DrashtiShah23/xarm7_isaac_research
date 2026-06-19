$Root = Split Path Parent (Split Path Parent $PSScriptRoot)
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join Path $Desktop "xArm7 Isaac Research.lnk"
$TargetPath = $Root
$WScriptShell = New Object ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $Root
$Shortcut.Save()
Write Host "Created desktop shortcut:"
Write Host $ShortcutPath
