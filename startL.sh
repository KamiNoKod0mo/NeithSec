# Esse script usa o nmap para scanear o host gerando um arquivo chamado scan
# Usamdo o tmux ele distribui os principais scripts na tela
# Esse script e os shell_scripts serão inutilizados, pois havera um interface web, sem a necessidade de gambiarras
if [ $# -eq 0 ]; then
    echo "Usage"
    echo "$0 8.8.8.8"
    exit 1
fi
    #comentado para otimizar teste, pois demora demais, sera futuramente eliminado.
    #./scan.sh $1 &

    #tmux kill-session
    tmux new -s Neith -d
    while [[ true ]]; do
        if [ -f "scan" ]; then

        tmux send-keys -t Neith "python3 functions/index.py -s exploit-db -nf scan -l 1 -w ${1}_mOn" C-m
        #substituir scan por scan_final se o de cima for descomentado

        tmux split-window -h
        tmux resize-pane -R 10

        tmux send-keys -t Neith 'python3 functions/monvirus.py' C-m

        tmux split-window -v

        tmux send-keys -t Neith 'python3 functions/monconnections.py' C-m

        tmux attach -t Neith
        break 
        
        else
            :
        fi
    done

# finaliza processo e excluir arquivos temporarios
tmux kill-session
rm -fr tmp/*
pkill scan.sh
pkill nmap
pkill sleep
rm -fr scan_final



    
    

