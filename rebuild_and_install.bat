@echo off
set ANDROID_HOME=C:\Users\deeh_\AppData\Local\Android\Sdk
set JAVA_HOME=C:\Progra~1\Eclipse Adoptium\jdk-17.0.19.10-hotspot
set ADB=C:\Users\deeh_\AppData\Local\Android\Sdk\platform-tools\adb.exe

set APK_PATH=C:\Users\deeh_\pizza-delivery\android\app\build\outputs\apk\debug\app-debug.apk

echo ========================================
echo  Pizza Boa - Rebuild and Install
echo ========================================
echo.

echo [1/2] Building APK...
cd /d C:\Users\deeh_\pizza-delivery\android
gradlew assembleDebug

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Build falhou! Verifique o log acima.
    pause
    exit /b 1
)

echo.
echo [2/2] Instalando no dispositivo...
%ADB% install -r %APK_PATH%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Instalacao falhou! Verifique se o emulador esta rodando.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Pronto! APK instalado com sucesso.
echo ========================================
pause
