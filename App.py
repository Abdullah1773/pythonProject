from flask import Flask, render_template, request, redirect, jsonify
from models import db, SEMM
# from convert import sql, json_data
from flask import jsonify




import sqlite3
import json
from flask import Flask, render_template, request, redirect, jsonify
from models import db, SEMM

# from convert import sql, json_data

from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import request

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SEMM.db' #name of database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db.init_app(app)

# app.before_request_funcs = [(None, db.create_all())]
# @app.before_first_request
# def create_table():
# db.create_all()

with app.app_context():
    # Code that needs application context
    db.create_all() # Example
# @app.before_first_request
# def create_table():
# db.create_all()
@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
            Activity = request.form.get('Activity', '')
            Explanation = request.form.get('Explanation', '')
            Artifacts = request.form.get('Artifacts', '')
            Method1 = request.form.get('Method1', '')
            Method2 = request.form.get('Method2', '')
            Method3 = request.form.get('Method3', '')
            System = SEMM(
                Activity = Activity,
                Explanation = Explanation,
                Artifacts = Artifacts,
                Method1 = Method1,
                Method2 = Method2,
                Method3 = Method3,
            )
            db.session.add(System)
            db.session.commit()
            return redirect('/')

@app.route('/', methods = ['GET']) #getiting datafrom here
def RetrieveList():
    System = SEMM.query.all()
    return render_template('index.html', System = System)
# return jsonify(json_data)

@app.route('/JSON_data', methods = ['GET']) #getiting datafrom here
def RetrievejsonData():

    db_path ='C:/Users/abdul/OneDrive/Desktop/Program/Project/pythonProject/.venv/var/App-instance/SEMM.db'

        # 'C:/Users/Abdullah/Desktop/Files/Project/pythonProject1/.venv/var/Appinstance/SEMM.db' # Note that you should specify the path of your database file here
    sql_query = "SELECT * FROM System" # SEMM
    json_data = fetch_data_as_json(db_path, sql_query)
    print(json_data)
    return json_data

def fetch_data_as_json(db_path, sql_query):
# Establish connection to the database
    conn = sqlite3.Connection(db_path)
    conn.row_factory = sqlite3.Row # Use row factory to get rows as dictionaries
    cursor = conn.cursor()
# Execute the SQL query
    cursor.execute(sql_query)
# Fetch all rows
    rows = cursor.fetchall()
# Convert each row to a dictionary
    data_list = [dict(row) for row in rows]
# Convert the list of dictionaries to JSON format
    json_data = json.dumps(data_list, indent=2)
    return json_data

@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    System = SEMM.query.filter_by(id=id).first()
    if request.method == 'POST':
        if System:
            db.session.delete(System)
            db.session.commit()
            return redirect('/')
        abort( 404 )
# return "Error: Student not found."
# else:
        return render_template('delete.html', System = System)

@app.route('/<int:id>/edit', methods=['POST'])
def update(id):
    System = SEMM.query.get(id)
    if not System:
        return f"System with id = {id} does not exist", 404
# Retrieve JSON data from the request body
    editedData = request.get_json()
# Update fields in the System object based on editedData
    System.Activity = editedData.get('Activity', '') if 'Activity' in editedData else ''
    System.Explanation = editedData.get('Explanation', '') if 'Explanation' in editedData else ''
    System.Artifacts = editedData.get('Artifacts', '') if 'Artifacts' in editedData else ''
    System.Method1 = editedData.get('Method1', '') if 'Method1' in editedData else ''
    System.Method2 = editedData.get('Method2', '') if 'Method2' in editedData else ''
    System.Method3 = editedData.get('Method3', '') if 'Method3' in editedData else ''
# Commit the changes to the database
    db.session.commit()
    return redirect('/')


app.run(debug=True, host='localhost', port=5006)



















#
# from flask import Flask, render_template, request, redirect, jsonify
# from models import db, SEMM
# # from convert import sql, json_data
# from flask import jsonify
#
# app = Flask(__name__)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SEMM.db'     #name of database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
# db.init_app(app)
#
# # app.before_request_funcs = [(None, db.create_all())]
# # @app.before_first_request
# # def create_table():
# #     db.create_all()
#
# with app.app_context():
#     # Code that needs application context
#     db.create_all()  # Example
# # @app.before_first_request
# # def create_table():
# #     db.create_all()
#
#
#
# @app.route('/create', methods = ['GET', 'POST'])
# def create():
#     if request.method == 'GET':
#         return render_template('create.html')
#
#     if request.method == 'POST':
#
#         Activity = request.form.get('Activity', '')
#         Explanation = request.form.get('Explanation', '')
#         Artifacts = request.form.get('Artifacts', '')
#         Methods = request.form.get('Methods', '')
#
#
#         System = SEMM(
#             Activity = Activity,
#             Explanation = Explanation,
#             Artifacts = Artifacts,
#             Methods = Methods
#         )
#         db.session.add(System)
#         db.session.commit()
#         return redirect('/')
#
# @app.route('/', methods = ['GET']) #getiting datafrom here
# def RetrieveList():
#     System = SEMM.query.all()
#     return render_template('index.html', System = System)
#     # return jsonify(json_data)
#
# # @app.route('/<int:id>/delete', methods=['GET','POST'])
# # def delete(id):
# #     students = StudentModel.query.filter_by(id=id).first()
# #     if request.method == 'POST':
# #         if students:
# #             db.session.delete(students)
# #             db.session.commit()
# #             return redirect('/')
# #             abort(404)
# #         return render_template('delete.html')
#
#
#
#
# @app.route('/<int:id>/delete', methods=['GET','POST'])
# def delete(id):
#     System = SEMM.query.filter_by(id=id).first()
#     if request.method == 'POST':
#         if System:
#             db.session.delete(System)
#             db.session.commit()
#             return redirect('/')
#         abort( 404 )
#     #         return "Error: Student not found."
#     # else:
#     return render_template('delete.html',  System = System)
#
# @app.route('/<int:id>/edit', methods=['GET', 'POST'])
# def update(id):
#     System = SEMM.query.get(id)
#     if request.method == 'POST':
#         if System:
#             System.Activity = request.form.get('Activity')
#             System.Explanation = request.form.get('Explanation')
#             System.Artifacts = request.form.get('Artifacts')
#             System.Methods = request.form.get('Methods')
#             db.session.commit()
#             return redirect('/')
#         else:
#             return f"Student with id = {Activity} does not exist"
#     return render_template('update.html', System = System)
#
#
#
#
# app.run(debug=True, host='localhost', port=5006)