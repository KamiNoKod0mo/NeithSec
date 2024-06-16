@echo off
REM Este script usa o nmap para escanear o host e gera um arquivo chamado scan
REM Usando o tmux, distribui os principais scripts na tela
REM Este script e os shell_scripts serão substituídos, pois haverá uma interface web, sem a necessidade de gambiarras

if "%~1"=="" (
    echo Uso:
    echo %~nx0 ^<IP_do_host^>
    exit /b 1
)

REM Comentado para otimizar o teste, pois demora muito, será eliminado futuramente.
REM start /B .\scan.bat %1

REM Finaliza sessão anterior do tmux, se houver
tmux kill-session >nul 2>&1

REM Cria nova sessão tmux chamada "Neith"
tmux new-session -d -s Neith

:LOOP
if exist "scan" (
    REM Executa os scripts em diferentes painéis do tmux
    tmux send-keys -t Neith "python3 functions/index.py -s exploit-db -nf scan -l 1 -w %1_mOn" Enter
    REM Substitua 'scan' por 'scan_final' se o anterior for descomentado

    tmux split-window -h
    tmux resize-pane -R 10

    tmux send-keys -t Neith "python3 functions/monvirus.py" Enter

    tmux split-window -v

    tmux send-keys -t Neith "python3 functions/monconnections.py" Enter

    tmux attach -t Neith
    exit /b
) else (
    timeout /t 1 >nul
    goto LOOP
)

REM Finaliza sessão do tmux e exclui arquivos temporários
tmux kill-session >nul 2>&1
del /q tmp\* >nul 2>&1
taskkill /f /im scan.bat >nul 2>&1
taskkill /f /im nmap.exe >nul 2>&1
taskkill /f /im sleep.exe >nul 2>&1
del /q scan_final >nul 2>&1
