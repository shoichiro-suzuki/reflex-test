python -m venv antenv
source antenv/bin/activate
pip install -r requirements.txt
python -m reflex run --env prod --backend-port 8000