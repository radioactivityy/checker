from flask import Flask,jsonify,request
import os,sys
import json

app=Flask(__name__)

DB_HOST='localhost'
DB_PORT=3306
DB_NAME='testdb'

def get_user(id,name,email,age,role,active):
    user={'id':id,'name':name,'email':email,'age':age,'role':role,'active':active}
    return user

def validate_email(email):
    if email==None:
        return False
    if '@' in email and '.' in email:
        return True
    else:
        return False

@app.route('/users',methods=['GET'])
def list_users():
    users=[
    {'id':1,'name':'Alice','email':'alice@example.com'},
    {'id':2,'name':'Bob','email':'bob@example.com'},
    {'id':3,'name':'Charlie','email':'charlie@example.com'}
    ]
    return jsonify(users)

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user_by_id(user_id):
    if user_id==None:
     return jsonify({'error':'Invalid ID'}),400
    if user_id>0:
            return jsonify({'id':user_id,'name':'Test User'})
    else:
        return jsonify({'error':'Not found'}),404

@app.route('/users',methods=['POST'])
def create_user():
    data=request.get_json()
    if data==None:
        return jsonify({'error':'No data'}),400
    name=data.get('name')
    email=data.get('email')
    if name==None or email==None:
        return jsonify({'error':'Missing fields'}),400
    if validate_email(email)==False:
        return jsonify({'error':'Bad email'}),400
    new_user={'id':99,'name':name,'email':email}
    return jsonify(new_user),201

def calculate_stats(numbers):
    total=0
    count=0
    for n in numbers:
        total=total+n
        count=count+1
    avg=total/count
    return {'total':total,'count':count,'avg':avg}

class UserManager:
    def __init__(self,db_host,db_port,db_name):
        self.db_host=db_host
        self.db_port=db_port
        self.db_name=db_name
        self.connection=None
        self.users=[]
        self.cache={}

    def connect( self ):
        print('Connecting to '+self.db_host+':'+str(self.db_port))
        self.connection=True

    def fetch_all(self):
        if self.connection==None:
            raise Exception('Not connected')
        return self.users

    def add_user(self,user):
        if user==None:
            return False
        self.users.append(user)
        return True


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)