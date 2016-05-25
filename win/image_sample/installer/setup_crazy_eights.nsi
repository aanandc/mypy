; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "Crazy Eights"

; The file to write
OutFile "Setup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\CrazyEights

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\CrazyEights" "Install_Dir"

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
Section "CrazyEights (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File "setup_crazy_eights.nsi"
  File /r "dist\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\CrazyEights "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CrazyEights" "DisplayName" "CrazyEights"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CrazyEights" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CrazyEights" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CrazyEights" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  ;MessageBox MB_OK "This is alpha quality software.Please do not use this for important financial calculations."
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\CrazyEights"
  CreateShortCut "$SMPROGRAMS\CrazyEights\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\CrazyEights\CrazyEights.lnk" "$INSTDIR\crazy.exe" "" "$INSTDIR\crazy.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CrazyEights"
  DeleteRegKey HKLM SOFTWARE\CrazyEights

  ; Remove files and uninstaller
  Delete $INSTDIR\setup_crazy_eights.nsi
  Delete $INSTDIR\uninstall.exe
 
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\CrazyEights\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\CrazyEights"
  RMDir /r "$INSTDIR"

SectionEnd
