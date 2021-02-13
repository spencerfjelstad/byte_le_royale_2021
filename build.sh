set echo off
rm -f *.pyz
cp -r ./game ./wrapper/game
python3.8 -m zipapp  ./wrapper -o ./launcher.pyz -c
rm -rf ./wrapper/game
