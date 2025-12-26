
; Inno Setup Script for QuantumQueue
[Setup]
AppName=QuantumQueue
AppVersion=2.0.1
AppPublisher=dianbrown
AppPublisherURL=https://github.com/dianbrown/CPU-SchedulingApp
DefaultDirName={autopf}\QuantumQueue
DefaultGroupName=QuantumQueue
OutputDir=dist\installers
OutputBaseFilename=QuantumQueue-2.0.1-Windows-Setup
SetupIconFile=Assets\Icons\app_icon.ico
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern
UninstallDisplayIcon={app}\QuantumQueue.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\QuantumQueue.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\QuantumQueue"; Filename: "{app}\QuantumQueue.exe"; IconFilename: "{app}\QuantumQueue.exe"
Name: "{autodesktop}\QuantumQueue"; Filename: "{app}\QuantumQueue.exe"; Tasks: desktopicon; IconFilename: "{app}\QuantumQueue.exe"

[Run]
Filename: "{app}\QuantumQueue.exe"; Description: "{cm:LaunchProgram,QuantumQueue}"; Flags: nowait postinstall skipifsilent
