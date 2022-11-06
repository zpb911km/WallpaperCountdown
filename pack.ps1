$FilePath = $PSScriptRoot + '\src\wallpaper.py'
$IconPath = $PSScriptRoot + '\icon.ico'
$WorkPath = $PSScriptRoot + '\build\work_folder'
$OutputPath = $PSScriptRoot + '\build\output'

pyinstaller $FilePath -D -w -i $IconPath --distpath $OutputPath --workpath $WorkPath --clean