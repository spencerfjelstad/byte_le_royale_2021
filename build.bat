
@echo off
del /q *.pyz

xcopy /s/e/i "game" "wrapper/game"
xcopy /s/e/i "server/client" "wrapper/server/client"
python -m zipapp "wrapper" -o "launcher.pyz"
del /q/s "wrapper/game"
del /q/s "wrapper/server/client"