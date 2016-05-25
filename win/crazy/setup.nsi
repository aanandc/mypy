
; example1.nsi
;
; This script is perhaps one of the simplest NSIs you can make. All of the
; optional settings are left to their default settings. The installer simply 
; prompts the user asking them where to install, and drops a copy of "MyProg.exe"
; there.

;--------------------------------

; The name of the installer
Name "Crazy Eights"

; The file to write
OutFile "setup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\sellsword_games

; The text to prompt the user to enter a directory
DirText "This will install my cool game in your PC. Choose a directory"

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

; Set output path to the installation directory.
SetOutPath $INSTDIR
CreateShortCut "$SMPROGRAMS\crazy.lnk" "$INSTDIR\crazy.exe"
; Put file there
File /r "E:\dev\python\crazy\dist\*"

SectionEnd ; end the section