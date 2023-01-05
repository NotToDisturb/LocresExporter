@echo off
set init_folder=locresexporter
set out_name=LocresExporter-standalone.zip
echo [INFO] CREATING %out_name%
del /Q .\build\*.* > nul
del /Q .\out\%out_name%
echo [INFO] Removed previous "out"
robocopy .\..\%init_folder% .\build __init__.py > nul
rename .\build\__init__.py %init_folder%.py
robocopy .\..\ .\build\ requirements.txt > nul
echo [INFO] Copied files
CScript  .\zip.vbs  .\build  .\out\%out_name% > nul
echo [INFO] Standalone zip created