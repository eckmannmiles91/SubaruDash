@echo off
REM Open KiCad Schematic Editor with software rendering (no OpenGL)
set LIBGL_ALWAYS_SOFTWARE=1
set KICAD_USE_EGL=0
start "" "C:\Program Files\KiCad\8.0\bin\eeschema.exe" "%~dp0wrx-power-can-hat-AUTO.kicad_sch"
