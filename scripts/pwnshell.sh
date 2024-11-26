#!/bin/bash

TEMP_PATH="$(realpath .)/pwn_template.py"
PICO_TEMP_PATH="$(realpath .)/pwn_template_tutorial.py"

export PYTHONSTARTUP=$(realpath .)/startup.py

alias sol="python3 solve.py"

function picostart() {
    cp -n $PICO_TEMP_PATH "${PWD}/solve.py"
    echo "Tutorial solve.py template created!"
}

# Copies pwn_template.py into pwd (no clobber)
function pwntemp() {
    cp -n $TEMP_PATH "${PWD}/solve.py"
    echo "solve.py template created!"
}

# Help creating payloads for format string attacks
function fspay() {
    PAY=""
    for i in {$1..$2} 
    do
        PAY+="%${i}\$p_"
    done
    echo $PAY
}

function start() {
    tmux new-session -d -s pat
    tmux split-window -h -p 75 -t pat
    tmux attach-session -t pat
}

function p() {
    python3 -c "print(\"$1\" * $2)"
}
