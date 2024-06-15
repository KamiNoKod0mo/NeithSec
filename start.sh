if [ $# -eq 0 ]; then
    echo "Usage"
    echo "$0 8.8.8.8"
    exit 1
fi
    #./scan.sh $1 &

    #tmux kill-session
    tmux new -s Neith -d
    while [[ true ]]; do
        if [ -f "scan" ]; then
        tmux send-keys -t Neith "python3 functions/index.py -s exploit-db -nf scan -l 2 -w ${1}_mOn" C-m

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
tmux kill-session
rm -fr tmp/*
pkill scan.sh
pkill nmap
pkill sleep
rm -fr scan_final



    
    

