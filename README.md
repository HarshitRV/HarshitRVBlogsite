# HarshitRV Blogsite (Blogging web app)
### Check [requirements](requirements.txt).

### Make sure to have [python3](https://www.python.org/downloads/) installed.
### Running on locally.
1. Create a virtual environment.
```bash
    python3 -m venv .venv
```
2. Activate the virtual environment.
```bash
    source venv/bin/activate
```
3. Create .env file
```bash
    touch .env
```
4. Add following environment variable
```bash
    SECRET_KEY=your_secret_key
    DB_URI=sqlite:///site.db
```
5. Install dependencies.
```bash
    pip install -r requirements.txt
```
6. Uncomment the line at 98 in [main.py](main.py), when running the server for first time for creating the database. (**Important:** Make sure to comment it again when its done, otherwise on every run new db will be created)

7. Run the application.
```bash
    python3 main.py
```