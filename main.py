from flask import Flask, request, render_template
import gspread
from google.oauth2 import service_account

app = Flask(__name__)

scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file('wlms-yearbook-checker-2020-908e386eb26f.json')
scoped_credentials = credentials.with_scopes(scopes)

gc = gspread.authorize(scoped_credentials)
student_ids = gc.open_by_key("1AKoY1sDPn9J4IZMXZlEMH_b8Vk55VR6XnasEIxBZ-BA").worksheet('Student IDs')


def check(student_id):
    try:
        student_ids.find(str(student_id), in_column=1)
        return True
    except gspread.exceptions.CellNotFound:
        return False


@app.route('/')
def index():
    student_id = request.args.get('id')

    if student_id and len(student_id) == 6 and student_id.isnumeric():
        valid = check(student_id)
        return render_template('index.html', valid=valid)
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
