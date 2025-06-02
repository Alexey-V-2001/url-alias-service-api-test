if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -d "venv" ]]; then
        echo "Virtual environment found. Activating..."
        source venv/bin/activate

        if [[ -z "$VIRTUAL_ENV" ]]; then
            echo "Failed to activate virtual environment."
            exit 1
        fi
    else
        echo "Virtual environment not found. Creating..."
        python -m venv venv

        echo "Activating..."
        source venv/bin/activate

        if [[ -z "$VIRTUAL_ENV" ]]; then
            echo "Failed to activate virtual environment after creation."
            exit 1
        fi
    fi
else
    echo "Virtual environment already activated."
fi

python3 check_dependencies.py

if [[ "$START" == "1" ]]; then
    echo "Running service..."
    #python3 main.py
fi

echo "Deactivating..."
deactivate
