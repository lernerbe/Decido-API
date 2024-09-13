# issac-service

1. ```python -m venv env``` 
2. ```pip install --no-cache-dir -r requirements.txt ```

to activate the virtual environment: ```source activate``` OR ```source env/Scripts/activate```
to disactivate the virtual environment: ```deactivate```

3. strat the server:
```uvicorn src.main:app --reload --port 8000```
open http://127.0.0.1:8000/docs

4. strat the server using docker:
``` docker compose up --build ```