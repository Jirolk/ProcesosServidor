@echo off
cd /d "D:\+-Documentos-CDS---\Factury\Python\ProcesosServidor"

echo Activando entorno virtual...
call env\Scripts\activate
echo Entorno virtual activado.

echo Ejecutando script de Python...
python main.py
echo Script de Python ejecutado.

echo Desactivando entorno virtual...
deactivate
echo Entorno virtual desactivado.

echo Finalizado.
pause
