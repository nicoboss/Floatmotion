; bigtest.nsi
;
; This script attempts to test most of the functionality of the NSIS exehead.

;--------------------------------

!ifdef HAVE_UPX
!packhdr tmp.dat "upx\upx -9 tmp.dat"
!endif

!ifdef NOCOMPRESS
SetCompress off
!endif

;--------------------------------

Name "Floatmotion"
Caption "Floatmotion - Nico Bosshard"
#Icon "${NSISDIR}\Contrib\Graphics\Icons\nsis1-install.ico"
Icon ".\img\Cube.ico"
OutFile "FloatmotionSetup.exe"
SetCompressor LZMA

SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
BGGradient 000000 800000 FFFFFF
InstallColors 80FF80 000030
XPStyle on

InstallDir "$PROGRAMFILES\Floatmotion"
InstallDirRegKey HKLM "Software\Floatmotion" "Install_Dir"

CheckBitmap "${NSISDIR}\Contrib\Graphics\Checks\classic-cross.bmp"

LicenseText "Floatmotion is a free open source software from Nico Bosshard made for a school project"
LicenseData "LICENSE"

RequestExecutionLevel admin

Var SelectionWarning_OK

;--------------------------------

Page license
Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

!ifndef NOINSTTYPES ; only if not defined
  InstType "Normal"
  InstType "Full"
  InstType "Base"
  ;InstType /NOCUSTOM
  ;InstType /COMPONENTSONLYONCUSTOM
!endif

AutoCloseWindow false
ShowInstDetails show

;--------------------------------


Section "Install Git Repository"
  SectionIn 1 2
  
  CreateDirectory "$INSTDIR\7-Zip"
  SetOutPath "$INSTDIR\7-Zip"
  File .\7-Zip\*
  SetOutPath $INSTDIR
  File ".\.git.7z"
  ExecWait '"$INSTDIR\7-Zip\7z.exe" x "$INSTDIR\.git.7z" -y'
  Delete "$INSTDIR\.git.7z"
  Sleep 100 # Only to be on the sure side.
  RMDir /r "$INSTDIR\7-Zip"
  File /a ".\.gitattributes"
  File /a ".\.gitignore"
SectionEnd


Section "" ; empty string makes it hidden, so would starting with -
  SetOutPath $INSTDIR
  WriteUninstaller "Uninstall.exe"

  ; write reg info
  WriteRegStr HKLM SOFTWARE\Floatmotion "Install_Dir" "$INSTDIR"

  ; write uninstall strings
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Floatmotion" "DisplayName" "Floatmotion (remove only)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Floatmotion" "UninstallString" '"$INSTDIR\Uninstall.exe"'
SectionEnd


Function .onSelChange
  StrCmp $SelectionWarning_OK "SelectionWarning_OK" +3 0
    MessageBox MB_OK|MB_ICONEXCLAMATION "Warning: Some of the packets you see on this page are required for my program. Unchek the requires ones only if you 100% understand what you are doing and have this packages already installed manually. For normal Users: Don't use the manually package selection. I made this page only for Developers!"
    StrCpy $SelectionWarning_OK "SelectionWarning_OK"
FunctionEnd


;--------------------------------

; Uninstaller

UninstallText "This will uninstall Floatmotion. Hit next to continue."
UninstallIcon "${NSISDIR}\Contrib\Graphics\Icons\nsis1-uninstall.ico"

Section "Uninstall"

  MessageBox MB_YESNO|MB_ICONQUESTION "Are you sure to completely uninstall Floatmotion from your computer?" IDNO NoDelete
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Floatmotion"
  DeleteRegKey HKLM "SOFTWARE\Floatmotion"
  RMDir /r "$INSTDIR"

  IfFileExists "$INSTDIR" 0 NoErrorMsg
    MessageBox MB_OK "Note: $INSTDIR could not be removed! Please delete it manually." IDOK 0 ; skipped if file doesn't exist

  NoErrorMsg:
  NoDelete:

SectionEnd
