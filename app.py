from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS

import uuid
import os
from dotenv import load_dotenv

load_dotenv()


app= Flask(__name__)
API_KEY=os.environ.get("API_KEY")
cors = CORS(app)
tasks=[]


def require_api(view_function):
    @wraps(view_function)

    def decorated_function(*args,**kwargs):
        if(request.args.get('key') and request.args.get('key')==API_KEY):
            return view_function(*args,**kwargs)
        else:
            return jsonify({'error':'api key is not correct.'}),401
    return decorated_function

@app.route('/',methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/',methods=['POST'])
@require_api
def new_task():
    if('description' not in request.form):
        print(request.args)
        return jsonify({'error':'Please add description.'}),401
    description=request.form['description']
    task={
        "id":str(uuid.uuid4()),
        "description":description,
        "completed":False
    }
    tasks.append(task)
    return jsonify(task)


@app.route('/delete',methods=['DELETE'])
@require_api
def delete():
    id=request.args.get('id')
    index=-1
    for i in range(len(tasks)):
        if(tasks[i]["id"]==id):
            index=i
            break
    if(index!=-1):
        tasks.pop(index)
        return jsonify({'result':True})
    else:
        return jsonify({'error':'id not found'}),401

@app.route('/update',methods=['PUT'])
@require_api
def update():
    id=request.args.get('id')
    for i in tasks:
        if(i["id"]==id):
            i["description"]=request.form['description']
            return jsonify(i)
    description=request.form['description']
    task={
        "id":str(uuid.uuid4()),
        "description":description,
        "completed":False
    }
    return jsonify(task)

@app.route('/toggle',methods=['PUT'])
@require_api
def toggle():
    id=request.args.get('id')
    flag=False
    for i in tasks:
        if(i["id"]==id):
            i["completed"]=not i["completed"]
            flag=True
            break
    if(flag):
        return jsonify("Status changed")
    else:
        return jsonify("id not found"),401

if __name__ =='__main__':
    app.run(debug=True,host='0.0.0.0')