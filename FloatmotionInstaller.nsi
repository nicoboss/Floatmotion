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

AutoCloseWindow true
ShowInstDetails show

;--------------------------------

Section "" ; empty string makes it hidden, so would starting with -
  SetOutPath $INSTDIR
  
  CreateDirectory "$INSTDIR\Fonts"
  CreateDirectory "$INSTDIR\img"
  CreateDirectory "$INSTDIR\obj"
  CreateDirectory "$INSTDIR\OpenGLLibrary"
  CreateDirectory "$INSTDIR\sound"
  CreateDirectory "$INSTDIR\textures"
  
  
  File /x FloatmotionSetup.exe /x python-2.7.7.msi /x config.ini /x FloatmotionInstaller.nsi /x FloatmotionInstaller.nsi /x .gitattributes /x .gitignore /x *.py *
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
  
  #The order here has nothing to do with the order NSIS write the file. NSIS make something (nearly) random what I don't understand but it's probably the time I added the line. So I sorted the following lines like NSIS does in the output file.
  WriteINIStr "$INSTDIR\config.ini"  "Info" "Version" "Floatmotion 1.0"
  WriteINIStr "$INSTDIR\config.ini"  "Info" "PublishDate" ${__DATE__}
  WriteINIStr "$INSTDIR\config.ini"  "Info" "Programmer" "Nico Bosshard"
  WriteINIStr "$INSTDIR\config.ini"  "Info" "E-Mail" "nico@bosshome.ch"
  
  CreateDirectory "$PICTURES\Floatmotion\"
  WriteINIStr "$INSTDIR\config.ini"  "Paths" "Screenshotpath" "$PICTURES\Floatmotion\"
  WriteINIStr "$INSTDIR\config.ini"  "Paths" "INSTDIR" "$INSTDIR"
  WriteINIStr "$INSTDIR\config.ini"  "Paths" "PROFILE" "$PROFILE"
  WriteINIStr "$INSTDIR\config.ini"  "Paths" "DOCUMENTS" "$DOCUMENTS"
  WriteINIStr "$INSTDIR\config.ini"  "Paths" "PICTURES" "$PICTURES"
  WriteINIStr "$INSTDIR\config.ini"  "Paths" "DESKTOP" "$DESKTOP"  
  WriteINIStr "$INSTDIR\config.ini"  "Graphics" "Fullscreen" "true"
  WriteINIStr "$INSTDIR\config.ini"  "Graphics" "noStars(more_FPS)" "false"
  WriteINIStr "$INSTDIR\config.ini"  "Graphics" "Screen_with" "1280"
  WriteINIStr "$INSTDIR\config.ini"  "Graphics" "Screen_high" "720"
  WriteINIStr "$INSTDIR\config.ini"  "Camera" "Camera_pos.x" "0"
  WriteINIStr "$INSTDIR\config.ini"  "Camera" "Camera_pos.y" "0.5"
  WriteINIStr "$INSTDIR\config.ini"  "Camera" "Camera_pos.z" "6"
  WriteINIStr "$INSTDIR\config.ini"  "Control" "MouseNoKlick(mouse Only)" "false"
  WriteINIStr "$INSTDIR\config.ini"  "Default" "EndlessMode" "false"
  WriteINIStr "$INSTDIR\config.ini"  "Default" "FastForward" "1.0"
  WriteINIStr "$INSTDIR\config.ini"  "Default" "Level" "1"
  WriteINIStr "$INSTDIR\config.ini"  "Default" "Lives" "7"
  WriteINIStr "$INSTDIR\config.ini"  "Default" "Level_length" "500"
  
  

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


Section "Install Python 2.7.7 (required)"
  SectionIn 1 2 3
  
  SetOutPath $INSTDIR
  
  IfFileExists "C:\Python27" 0 +3
    MessageBox MB_OK "Python 2.7.7 is already installed under C:\Python27\ you don't need it again." IDOK 0 ; skipped if file doesn't exist
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




Section "Open Help file after setup"
  SectionIn 1 2
  ExecShell "open" '"$INSTDIR\Help.mht"'
SectionEnd


Section "Start Floatmotion after setup"

  SectionIn 1 2

  #Exec '"$INSTDIR\main.py"'
  Sleep 250
  ExecShell "open" '"$INSTDIR\main.pyc"'
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
