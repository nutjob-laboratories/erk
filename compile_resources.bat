
del ./erk/resources.py

cd resources

python build_resources.py > resources.qrc

pyrcc5 -o resources.py resources.qrc
move /Y resources.py ../erk/data/resources.py

del resources.qrc

cd ..

del ./erk/erkimg.py

cd erkresource

python build_resources.py > resources.qrc

pyrcc5 -o erkimg.py resources.qrc
move /Y erkimg.py ../erk/data/erkimg.py

del resources.qrc

cd ..
