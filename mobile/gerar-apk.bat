@echo off
echo ========================================
echo   Pizza Boa - Gerar APK
echo ========================================
echo.

cd /d C:\Users\deeh_\pizza-delivery\mobile

echo [1/3] Sincronizando Capacitor...
call npx cap sync android
echo.

echo [2/2] Gerando APK...
cd android
call gradlew assembleDebug
echo.

if exist app\build\outputs\apk\debug\app-debug.apk (
    echo ========================================
    echo   APK GERADO COM SUCESSO!
    echo ========================================
    echo.
    echo Localizacao: android\app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo Para instalar no celular:
    echo   1. Copie o APK para o celular
    echo   2. Habilite "Fontes desconhecidas" nas configuracoes
    echo   3. Abra o arquivo APK e instale
) else (
    echo Erro ao gerar APK. Verifique se o Android Studio esta instalado.
)

pause
