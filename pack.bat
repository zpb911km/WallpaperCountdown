@echo off

set FilePath=%~DP0src\wallpaper.py
set IconPath=%~DP0icon.ico
set WorkPath=%~DP0build\work_folder
set OutputPath=%~DP0build\output

pyinstaller %FilePath% -D -w -i %IconPath% --distpath %OutputPath% --workpath %WorkPath% --clean