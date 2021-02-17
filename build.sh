set echo off
rm -f *.pyz
cp -r ./game ./wrapper/game
cp -r  ./scrimmage ./wrapper/scrimmage
python3.8 -m zipapp  ./wrapper -o ./launcher.pyz -c
rm -rf ./wrapper/game
rm -rf ./wrapper/scrimmage
