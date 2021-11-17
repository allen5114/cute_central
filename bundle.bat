REM This file creates a bundle folder which we can zip up to deploy on AWS

REM clear the old bundle folder
rmdir /S .\bundle\ /q /s

REM create needed folders
mkdir .\bundle
mkdir .\bundle\.ebextensions
mkdir .\bundle\config
mkdir .\bundle\utils
mkdir .\bundle\assets

REM copy over the files
xcopy .\.ebextensions .\bundle\.ebextensions /E /Y
xcopy .\config .\bundle\config /E /Y
xcopy .\utils .\bundle\utils /E /Y
xcopy .\assets .\bundle\assets /E /Y

xcopy .\app_base.py .\bundle\ /Y
xcopy .\app_prod.py .\bundle\ /Y
xcopy .\requirements.txt .\bundle\ /Y
xcopy .\youtube_api.py .\bundle\ /Y

REM remove unneeded files
rmdir /S .\bundle\assets\js /q /s
rmdir /S .\bundle\utils\__pycache__ /q /s

cd bundle
tar.exe -a -cf ../aws_deploy.zip *
cd ..

rmdir /S .\bundle /q /s
