@echo off
cd /d "c:\Users\Lenovo\Documents\GitHub\zatoona\android"
set "JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot"
set "ANDROID_HOME=C:\Users\Lenovo\AppData\Local\Android\Sdk"
set "GRADLE_OPTS=-Xmx2048m -Dfile.encoding=UTF-8"
"C:\Users\Lenovo\AppData\Local\Gradle\gradle-8.5\bin\gradle.bat" assembleDebug
