
rem @echo off
rem call "C:\Program Files\QGIS 3.0\bin\o4w_env.bat"
rem call "C:\Program Files\QGIS 3.0\bin\qt5_env.bat"
rem call "C:\Program Files\QGIS 3.0\bin\py3_env.bat"

rem @echo on

del ./erk/resources.py

cd resources

python build_resources.py > resources.qrc

pyrcc5 -o resources.py resources.qrc
move /Y resources.py ../erk/resources/resources.py

del resources.qrc

cd ..

