; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

; Versioning
; we do some #ifdef conditionals because automated compilation passes these as arguments

#ifndef MyAppVersion
    #define MyAppVersion "2.1.0"
#endif

; Other config

#define MyAppName "pyfa"
#define MyAppPublisher "pyfa"
#define MyAppURL "https://github.com/pyfa-org/Pyfa/"
#define MyAppExeName "pyfa.exe"

#ifndef MyOutputFile
    #define MyOutputFile LowerCase(StringChange(MyAppName+'-'+MyAppVersion+'-win', " ", "-"))
#endif
#ifndef MyAppDir
    #define MyAppDir "pyfa"
#endif
#ifndef MyOutputDir
    #define MyOutputDir "dist"
#endif

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{3DA39096-C08D-49CD-90E0-1D177F32C8AA}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
CloseApplications=yes
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile={#MyAppDir}\LICENSE
OutputDir={#MyOutputDir}
OutputBaseFilename={#MyOutputFile}
SetupIconFile={#MyAppDir}\pyfa.ico
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "{#MyAppDir}\pyfa.exe"; DestDir: "{app}"; Flags: ignoreversion; AfterInstall: RemoveFromVirtualStore
Source: "{#MyAppDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[InstallDelete]
; These will delete left over generated files from 1.14 and below
Type: filesandordirs; Name: "{app}\eos"
Type: filesandordirs; Name: "{app}\gui"
Type: filesandordirs; Name: "{app}\service"
Type: filesandordirs; Name: "{app}\utils"
Type: files; Name: "{app}\*.pyo"
Type: files; Name: "{app}\*.pyc"

[Code]

/////////////////////////////////////////////////////////////////////
function IsAppRunning(const FileName : string): Boolean;
var
    FSWbemLocator: Variant;
    FWMIService   : Variant;
    FWbemObjectSet: Variant;
begin
    Result := false;
    FSWbemLocator := CreateOleObject('WBEMScripting.SWBEMLocator');
    FWMIService := FSWbemLocator.ConnectServer('', 'root\CIMV2', '', '');
    FWbemObjectSet := FWMIService.ExecQuery(Format('SELECT Name FROM Win32_Process Where Name="%s"',[FileName]));
    Result := (FWbemObjectSet.Count > 0);
    FWbemObjectSet := Unassigned;
    FWMIService := Unassigned;
    FSWbemLocator := Unassigned;
end;

/////////////////////////////////////////////////////////////////////
procedure RemoveFromVirtualStore;
var
    VirtualStore,FileName,FilePath:String;
    DriveChars:Integer;
begin
    VirtualStore:=AddBackslash(ExpandConstant('{localappdata}'))+'VirtualStore';
    FileName:=ExpandConstant(CurrentFileName);
    DriveChars:=Length(ExtractFileDrive(FileName));
    if DriveChars>0 then begin
        Delete(FileName,1,DriveChars);
        FileName:=VirtualStore+FileName;
        FilePath:=ExtractFilePath(FileName);
        DelTree(FilePath, True, True, True);
    end;
end;

/////////////////////////////////////////////////////////////////////
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  if(IsAppRunning( 'pyfa.exe' )) then
    begin
      Result := 'Please close pyfa before continuing. When closed, please go back to the previous step and continue.';
    end
  else
    begin
      Result := '';
    end
end;

/////////////////////////////////////////////////////////////////////
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{{3DA39096-C08D-49CD-90E0-1D177F32C8AA}_is1'); //Your App GUID/ID
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    if not RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString) then
      if not RegQueryStringValue(HKLM32, sUnInstPath, 'UninstallString', sUnInstallString) then
        RegQueryStringValue(HKCU32, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

/////////////////////////////////////////////////////////////////////
function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
// Return Values:
// 1 - uninstall string is empty
// 2 - error executing the UnInstallString
// 3 - successfully executed the UnInstallString

  // default return value
  Result := 0;

  // get the uninstall string of the old app
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

/////////////////////////////////////////////////////////////////////
function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

/////////////////////////////////////////////////////////////////////
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;
