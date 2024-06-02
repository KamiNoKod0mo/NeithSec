if [ $# -eq 0 ]; then
    echo "Usage"
    echo "$0 8.8.8.8"
    exit 1
fi
    ./scan.sh $1 &

    #tmux kill-session
    tmux new -s Seith -d
    while [[ true ]]; do
        if [ -f "scan_final" ]; then
        tmux send-keys -t Seith "python3 mOnVulns.py -s exploit-db -nf scan_final -l 2 -w ${1}_mOn" C-m

        tmux split-window -h
        tmux resize-pane -R 10
        tmux send-keys -t Seith 'python3 monfile.py' C-m

        tmux split-window -v
        tmux send-keys -t Seith 'python3 moncon.py' C-m

        tmux attach -t Seith
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



    
    

