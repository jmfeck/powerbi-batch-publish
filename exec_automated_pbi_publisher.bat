::Step 1 - Copying files to from pbi_publish
cd /d "%~dp0"

set "SOURCE_FOLDER=..\..\..\processes\pbi_publish"
set "DESTINATION_FOLDER=.\input"

echo Copying files from "%SOURCE_FOLDER%" to "%DESTINATION_FOLDER%"...
move /Y "%SOURCE_FOLDER%\*.pbix" "%DESTINATION_FOLDER%\"

::Step 2 - Executing Publishing
call activate sandbox
::python scripts/autogui_pbi_publisher.py
python scripts/powershell_pbi_publisher.py

::Step 3 - Copying files from pbi_publish/published
cd /d "%~dp0"

set "SOURCE_FOLDER=.\output"
set "DESTINATION_FOLDER=..\..\..\processes\pbi_publish\published"

echo Copying files from "%SOURCE_FOLDER%" to "%DESTINATION_FOLDER%"...
move /Y "%SOURCE_FOLDER%\*.pbix" "%DESTINATION_FOLDER%\"

::PAUSE