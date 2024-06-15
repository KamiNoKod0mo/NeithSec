#!/bin/bash
while [[ true ]]; do
    nmap -sS -sV -O -oX scan -Pn $1 > /dev/null
    wait
    cat scan > scan_final
    sleep 20
done

