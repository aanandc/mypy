; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "MouseMover"

; The file to write
OutFile "Setup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\MouseMover

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\MouseMover" "Install_Dir"

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
Section "MouseMover (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File "setup_mouse_mover.nsi"
  File /r "dist\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\MouseMover "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MouseMover" "DisplayName" "MouseMover"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MouseMover" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MouseMover" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MouseMover" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  MessageBox MB_OK "Common use - Avoid screen to be locked by moving around the mouse every ten seconds without disturbing the user"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\MouseMover"
  CreateShortCut "$SMPROGRAMS\MouseMover\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\MouseMover\MouseMover.lnk" "$INSTDIR\mouse_mover.exe" "" "$INSTDIR\mouse_mover.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MouseMover"
  DeleteRegKey HKLM SOFTWARE\MouseMover

  ; Remove files and uninstaller
  Delete $INSTDIR\setup_mouse_mover.nsi
  Delete $INSTDIR\uninstall.exe
 
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\MouseMover\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\MouseMover"
  RMDir /r "$INSTDIR"

SectionEnd
