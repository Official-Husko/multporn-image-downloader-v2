@echo off
set NLM=^


set NL=^^^%NLM%%NLM%^%NLM%%NLM%
set /p file= .ui file name? %NL%
pyinstaller --onefile -w -i "icon.ico" %file%
set /p end= Done, press ENTER to quit