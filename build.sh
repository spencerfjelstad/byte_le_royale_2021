set echo off
rm -f *.pyz
cp -r ./game ./wrapper/game
cp -r  ./scrimmage ./wrapper/scrimmage
<<<<<<< HEAD
python3.8 -m zipapp  ./wrapper -o ./launcher.pyz -c
=======
python3 -m zipapp  ./wrapper -o ./launcher.pyz -c
>>>>>>> 64e0112d1f24b83df3e2e279d4f8a07e4014d9ff
rm -rf ./wrapper/game
rm -rf ./wrapper/scrimmage
