@echo off
REM Open KiCad Schematic Editor with the FIXED schematic
set LIBGL_ALWAYS_SOFTWARE=1
set KICAD_USE_EGL=0
start "" "C:\Program Files\KiCad\9.0\bin\eeschema.exe" "%~dp0wrx-power-can-hat-FIXED.kicad_sch"
