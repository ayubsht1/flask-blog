#run the following commands after downloading the code
pip install -r requirements.txt
set FLASK_APP=run.py
#database codes
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask run 