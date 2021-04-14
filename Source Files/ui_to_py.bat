@echo off
set NLM=^


set NL=^^^%NLM%%NLM%^%NLM%%NLM%
set /p file= .ui file name? %NL%
pyuic5 %file% > out.py 
set /p end= Done, press ENTER to quit