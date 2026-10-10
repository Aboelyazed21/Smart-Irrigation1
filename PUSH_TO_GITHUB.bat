@echo off
REM One-click upload to https://github.com/Aboelyazed21/Smart-Irrigation1
REM Run this file on your own PC (double-click). Requires git login once.
cd /d "%~dp0"
git init 2>nul
git branch -M main 2>nul
git remote remove origin 2>nul
git remote add origin https://github.com/Aboelyazed21/Smart-Irrigation1.git
git add .
git commit -m "CSC4103 PS1 Parts B+C: robust controller, approval gate, autonomy levels, smart irrigation + report" 2>nul
git push -u origin main
pause
