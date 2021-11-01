# Check [requirements](requirements.txt).
# Running on local server.
1. Create a virtual environment.
```bash
    python3 -m venv venv
```
2. Activate the virtual environment.
```bash
    source venv/bin/activate
```
3. Install dependencies.
```bash
    pip install -r requirements.txt
```
4. Uncomment the line at 98 in [main.py](main.py), when running the server for first time for creating the database.

5. Run the application.
```bash
    python3 main.py
```
6. Once the server starts comment the line at 98 in [main.py](main.py). As we no longer need it since the database has been created after first spin of the server.
