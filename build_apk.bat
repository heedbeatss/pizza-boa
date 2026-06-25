@echo off
set ANDROID_HOME=C:\Users\deeh_\AppData\Local\Android\Sdk
set JAVA_HOME=C:\Progra~1\Eclipse Adoptium\jdk-17.0.19.10-hotspot
cd /d C:\Users\deeh_\pizza-delivery\android
gradlew clean
gradlew assembleDebug
gradlew :capacitor-local-notifications:assembleDebug --no-build-cache
gradlew assembleDebug
