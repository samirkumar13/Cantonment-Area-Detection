; CantonmentAreaDetectionInstaller.iss
; Installer for "Cantonment Area Detection"

[Setup]
AppName=Cantonment Area Detection
; Optional version (kept minimal for stability)
AppVersion=1.0.0.0
AppPublisher=LoQ
OutputDir=.
; Installer output filename will be: "Cantonment Area Detection.exe"
OutputBaseFilename=Cantonment Area Detection
; Installer icon file - must exist next to this .iss or use full path
SetupIconFile=icon.ico

; Install location and UI
DefaultDirName={pf}\Splasher
DefaultGroupName=Cantonment Area Detection
DisableDirPage=no
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern

[Files]
; Main PyInstaller build output folder
Source: "C:\Users\Samir\Desktop\Splasher\dist\Splasher\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Ensure icon is copied (for shortcut icon)
Source: "C:\Users\Samir\Desktop\Splasher\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut
Name: "{group}\Cantonment Area Detection"; Filename: "{app}\Splasher.exe"; IconFilename: "{app}\icon.ico"
; Desktop shortcut (optional, selectable)
Name: "{commondesktop}\Cantonment Area Detection"; Filename: "{app}\Splasher.exe"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
; Run the app after install
Filename: "{app}\Splasher.exe"; Description: "Run Cantonment Area Detection"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
