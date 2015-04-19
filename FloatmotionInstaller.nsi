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

AutoCloseWindow true
ShowInstDetails show

;--------------------------------

Section "" ; empty string makes it hidden, so would starting with -
  RMDir "$TEMP\SelectionWarning_OK\"
  SetOutPath $INSTDIR
  
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
  SectionIn 1 2
  SetOutPath $INSTDIR
  File /r *.py
SectionEnd


Section "Install Python 2.7.7 (required)"
  SectionIn 1 2 3
  
  SetOutPath $INSTDIR
  
  IfFileExists "C:\Python27" 0 +3
    MessageBox MB_OK "Python 2.7.7 is already installed under C:\Python27\ you don't need this again." IDOK 0 ; skipped if file doesn't exist
    Goto Skip_Pyhon77
  File python-2.7.7.msi
  ExecShell "open" '"$INSTDIR\python-2.7.7.msi"'
  Skip_Pyhon77:

SectionEnd


SectionGroup /e "Install required Libraries"
Section "pygame"
  SectionIn 1 2 3
  
  SetOutPath $INSTDIR
  File /r .\pygame\

SectionEnd

Section "pyOpenGL"

  SectionIn 1 2 3
  
  SetOutPath $INSTDIR
  File /r .\OpenGL\

SectionEnd
SectionGroupEnd

SectionGroup /e "Shortcuts"
Section "Desktop"
  SectionIn 1 2

  SetOutPath $INSTDIR ; for working directory
  CreateShortcut "$DESKTOP\Floatmotion.lnk" "$INSTDIR\main.pyc" "" "$INSTDIR\img\Cube.ico" 0 SW_SHOWMINIMIZED
SectionEnd

Section "Startprograms"
  SectionIn 1 2

  SetOutPath $INSTDIR ; for working directory
  CreateShortcut "$SMPROGRAMS\Floatmotion.lnk" "$INSTDIR\main.pyc" "" "$INSTDIR\img\Cube.ico" 0 SW_SHOWMINIMIZED
SectionEnd
SectionGroupEnd



Section "Start Floatmotion after setup" TESTIDX

  SectionIn 1 2

  #Exec '"$INSTDIR\main.py"'
  ExecShell "open" '"$INSTDIR\main.pyc"'
  #ExecShell "open" '"$INSTDIR"'
SectionEnd

Section "Open Help file after setup" TESTIDX

  SectionIn 1 2

  #Exec '"$INSTDIR\main.py"'
  ExecShell "open" '"$INSTDIR\Help.mht"'
  #ExecShell "open" '"$INSTDIR"'
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
  #StrCmp $0 "SelectionWarning_OK" +3 0 ; Doesn't works do to only local variables.
  IfFileExists "$TEMP\SelectionWarning_OK" +3 0
    MessageBox MB_OK|MB_ICONEXCLAMATION "Warning: Some of the packets you see on this page are required for my program. Unchek the requires ones only if you 100% understand what you are doing and have this packages already installed manually. For normal Users: Don't use the manually package selection. I made this page only for Developers!"
    CreateDirectory "$TEMP\SelectionWarning_OK"
    #StrCpy $0 "SelectionWarning_OK"
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
