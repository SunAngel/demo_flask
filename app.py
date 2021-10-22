from flask import Flask, jsonify, request
import logging

app = Flask(__name__) #creating the Flask class object   
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

booklist = [
    {
        "author": "Coreman",
        "title": "Algorithem"
    },
    {
        "author": "navathe",
        "title": "Database Fundamentals"
    },
    {
        "author": "ritchie",
        "title": "Let us C"
    }
]

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        queryData = request.args.get('name')
        
      #  data = "hello world" +' ' + queryData
        return jsonify({'data': queryData  })

@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
  
    return jsonify({'data': num**2})


@app.route("/v1/books/",  methods = ['GET'])
def list_all_books():
    app.logger.info('Retrieving list of all books')
    list = []
    app.logger.info("list , iterating book list")
    for item in booklist:
      list.append({'book':item['title']}) 
    return jsonify(list)

@app.route("/v1/books/delete", methods=['DELETE'])
def delete_book():
    return jsonify({'message': 'Delete book successfully'}),200

@app.route("/v1/books/update", methods=['PUT'])
def update_book():
    return jsonify({'message': 'Update book successfully'}),200

@app.route("/v1/books/add", methods=['POST'])
def add_book():
    author = request.json.get('author')
    book = request.json.get('title')
    if not author or not book:
        return jsonify({'error': 'Please provide Author and Title'}), 400
    else:
        data = request.get_json()
        booklist.append(data)
        return jsonify({'message': 'Added book successfully','author':author,'book': book}),200
   

@app.route("/v1/books/<string:author>", methods=["GET"])
def get_by_author(author):
    app.logger.info('Getting book by Author')
    data = None
    for item in booklist:
	    if item['author'] == author:
                data = item
                return jsonify(data)
    if not data:
        return jsonify({'error': 'Author does not exist'}), 404

if __name__ =='__main__':  
    app.run(debug = True) 