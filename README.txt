# Steam Games Search Engine

## How to run

You can run the frontend with the command
```bash
cd ui
npm install
npm run serve
```

The python backend also must also be running.

Run command:
```bash
cd api
pip install -r requirements.txt
python wsgi.py
# OR
gunicorn --bind :5000 --workers 1 --threads 8 --timeout 0 api:app
```