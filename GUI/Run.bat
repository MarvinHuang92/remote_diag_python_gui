@echo off

if exist "D:\Program Files\Python36\python.exe" set py3="D:\Program Files\Python36\python.exe"
if exist "C:\TCC\Tools\python3\3.6.5-6_WIN64\python.exe" set py3="C:\TCC\Tools\python3\3.6.5-6_WIN64\python.exe"
%py3% GUI.py

pause