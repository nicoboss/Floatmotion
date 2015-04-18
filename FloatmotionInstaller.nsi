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
Icon "${NSISDIR}\Contrib\Graphics\Icons\nsis1-install.ico"
OutFile "FloatmotionSetup.exe"
SetCompressor LZMA

SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
BGGradient 000000 800000 FFFFFF
InstallColors FF8080 000030
XPStyle on

InstallDir "$PROGRAMFILES\Floatmotion"
InstallDirRegKey HKLM "Software\Floatmotion" "Install_Dir"

CheckBitmap "${NSISDIR}\Contrib\Graphics\Checks\classic-cross.bmp"

LicenseText "Floatmotion is a free open surce software from Nico Bosshard made for a school project"
LicenseData "LICENSE"

RequestExecutionLevel admin

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
  InstType "More"
  InstType "Base"
  ;InstType /NOCUSTOM
  ;InstType /COMPONENTSONLYONCUSTOM
!endif

AutoCloseWindow false
ShowInstDetails show

;--------------------------------
MessageBox MB_OK "WriteINIStr failed"

Section "" ; empty string makes it hidden, so would starting with -
  SetOutPath $INSTDIR

  CreateDirectory "$INSTDIR\alt"
  CreateDirectory "$INSTDIR\Fonts"
  CreateDirectory "$INSTDIR\img"
  CreateDirectory "$INSTDIR\obj"
  CreateDirectory "$INSTDIR\OpenGLLibrary"
  CreateDirectory "$INSTDIR\sound"
  CreateDirectory "$INSTDIR\textures"
  
  
  File /x FloatmotionSetup.exe /x python-2.7.7.msi /x *.py *
  SetOutPath $INSTDIR\Fonts
  File .\Fonts\*
  SetOutPath $INSTDIR\img
  File .\img\*
  SetOutPath $INSTDIR\obj
  File .\obj\*
  SetOutPath $INSTDIR\OpenGLLibrary
  File /x *.py .\OpenGLLibrary\*
  SetOutPath $INSTDIR\sound
  File .\sound\*
  SetOutPath $INSTDIR\textures
  File .\textures\*

  SetOutPath $INSTDIR
  ; write reg info
  WriteRegStr HKLM SOFTWARE\Floatmotion "Install_Dir" "$INSTDIR"

  ; write uninstall strings
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Floatmotion" "DisplayName" "Floatmotion (remove only)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Floatmotion" "UninstallString" '"$INSTDIR\Uninstall.exe"'

  
  WriteUninstaller "Uninstall.exe"

SectionEnd


Section "Install Source Code"

  SectionIn 1 2 3
  SetOutPath $INSTDIR
  File /r /x FloatmotionSetup.exe /x python-2.7.7.msi /x *.py *

SectionEnd


Section "Install Python 2.7.7 (required)"

  SectionIn 1 2 3 4
  
  SetOutPath $INSTDIR
  File python-2.7.7.msi

  SetOutPath $INSTDIR\cpdest
  CopyFiles "$WINDIR\*.ini" "$INSTDIR\cpdest" 0

SectionEnd

SectionGroup /e "Install required Libarries"

Section "pygame"

  SectionIn 1 2 3 4
  
  SetOutPath $INSTDIR\pygame
  File /r .\pygame\

SectionEnd

Section "pyOpenGL"

  SectionIn 1 2 3 4
  
  SetOutPath $INSTDIR\OpenGL
  File /r .\OpenGL\

SectionEnd
SectionGroupEnd

SectionGroup /e "Shortcuts"

Section "Desktop"

  SectionIn 1 2 3

  SetOutPath $INSTDIR ; for working directory
  CreateShortcut "$DESKTOP\Uninstall Floatmotion.lnk" "$INSTDIR\Uninstall.exe" ; use defaults for parameters, icon, etc.

SectionEnd

Section "Startprograms"

  SectionIn 1 2 3

  CreateDirectory "$SMPROGRAMS\Floatmotion"
  SetOutPath $INSTDIR ; for working directory
  CreateShortcut "$SMPROGRAMS\Floatmotion\Uninstall Floatmotion.lnk" "$INSTDIR\Uninstall.exe" ; use defaults for parameters, icon, etc.
SectionEnd
SectionGroupEnd



Section "Start Floatmotion after setup" TESTIDX

  SectionIn 1 2 3

  #Exec '"$INSTDIR\main.py"'
  ExecShell "open" '"$INSTDIR\main.py"'
  ExecShell "open" '"$INSTDIR"'
  Sleep 500
  BringToFront

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

  SectionGetText ${TESTIDX} $0
  StrCmp $0 "" e
    SectionSetText ${TESTIDX} ""
  Goto e2
e:
  SectionSetText ${TESTIDX} "TextInSection"
e2:

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
    MessageBox MB_OK "Note: $INSTDIR could not be removed!" IDOK 0 ; skipped if file doesn't exist
	
  NoErrorMsg:
  NoDelete:

SectionEnd
