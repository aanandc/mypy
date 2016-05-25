; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "Compount Interest"

; The file to write
OutFile "Setup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\CompoundInterest

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\CompountInterest" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "CompountInterest (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File "setup_ci.nsi"
  File /r "dist\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\CompoundInterest "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CompoundInterest" "DisplayName" "CompoundInterest"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CompoundInterest" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CompoundInterest" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CompoundInterest" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  MessageBox MB_OK "This is alpha quality software.Please do not use this for important financial calculations."
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\CompoundInterest"
  CreateShortCut "$SMPROGRAMS\CompoundInterest\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\CompoundInterest\CompoundInterest.lnk" "$INSTDIR\interest.exe" "" "$INSTDIR\interest.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CompoundInterest"
  DeleteRegKey HKLM SOFTWARE\CompoundInterest

  ; Remove files and uninstaller
  Delete $INSTDIR\setup_ci.nsi
  Delete $INSTDIR\uninstall.exe
 
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\CompoundInterest\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\CompoundInterest"
  RMDir /r "$INSTDIR"

SectionEnd
