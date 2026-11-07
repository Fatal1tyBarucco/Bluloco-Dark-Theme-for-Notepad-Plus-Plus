@echo off
:: Sample Batch code to test Bluloco Dark
echo Starting theme check...

set THEME_NAME=BlulocoDark.xml
if exist %THEME_NAME% (
    echo Found %THEME_NAME%
) else (
    echo %THEME_NAME% not found
    exit /b 1
)

pause
