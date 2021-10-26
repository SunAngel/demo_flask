from flask import Flask, jsonify, request
import logging
import psycopg2
from psycopg2.errors import SerializationFailure

app = Flask(__name__) #creating the Flask class object   

logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


with conn.cursor() as cur:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Employee (id INT PRIMARY KEY, Name STRING)"
    )
    cur.execute(
        "UPSERT INTO Employee (id, Name) VALUES (1, 'Aman'), (2, 'Deeksha'), (3,'Pooja')"
    )
conn.commit()    

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        queryData = request.args.get('name')
        
      #  data = "hello world" +' ' + queryData
        return jsonify({'data': queryData  })

@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
  
    return jsonify({'data': num**2})


@app.route("/v1/employee/",  methods = ['GET'])
def list_all_books():
    app.logger.info('Retrieving list of all books')
    with conn.cursor() as cur:
        cur.execute("SELECT id, Name FROM Employee")
        rows = cur.fetchall()
        conn.commit()
        my_list = []
        for row in rows:
            my_list.append({"id":row[0], "name": row[1]})
    return jsonify(my_list)

@app.route("/v1/employee/delete", methods=['DELETE'])
def delete_employee():
    id = request.json.get('id')
   
    if not id :
        return jsonify({'error': 'Please provide Id'}), 400
    else:
       with conn.cursor() as cur:
        cur.execute(
            "Delete from Employee  where id = {}".format(id)
        )
        conn.commit()
        return jsonify({'message': 'Delete from Employee successfully','id':id}),200

@app.route("/v1/employee/update", methods=['PUT'])
def update_employee():
    id = request.json.get('id')
    name = request.json.get('name')
    if not id or not name:
        return jsonify({'error': 'Please provide Id and Name'}), 400
    else:
       with conn.cursor() as cur:
        cur.execute(
            "Update  Employee set name = '{}' where id = {}".format(name,id)
        )
        conn.commit()
        return jsonify({'message': 'Update Employee successfully','id':id,'name': name}),200

@app.route("/v1/employee/add", methods=['POST'])
def add_employee():
    id = request.json.get('id')
    name = request.json.get('name')
    if not id or not name:
        return jsonify({'error': 'Please provide Id and Name'}), 400
    else:
       with conn.cursor() as cur:
        cur.execute(
            "UPSERT  into  Employee Values ({},'{}')".format(id,name)
        )
        conn.commit()
        return jsonify({'message': 'Added Employee successfully','id':id,'name': name}),200
   

@app.route("/v1/employee/<int:id>", methods=["GET"])
def get_by_id(id):
    app.logger.info('Getting Employee by Id')
    data = None
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM employee WHERE id = {}".format(id))
        row = cur.fetchone()
        conn.commit()
    if not row:
        return jsonify({'error': 'Author does not exist'}), 404
    else:
        data = {"id" :row[0], "name": row[1]}
        return jsonify(data)

if __name__ =='__main__':  
    app.run(debug = True) 