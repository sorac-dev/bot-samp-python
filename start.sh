#!/bin/bash

while true; do
    python3 main.py
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "El bot se ha cerrado correctamente."
        exit 0
    else
        echo "El bot se ha cerrado con el código de error $exit_code. Reiniciando..."
        sleep 5
    fi
done
