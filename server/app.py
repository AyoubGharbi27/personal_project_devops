import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

# Configuration
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})  # Enhanced CORS for Docker

# In-memory data store (unchanged)
BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    # ... (other books remain identical)
]

# Helper function (unchanged)
def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

# Routes with Docker-compatible responses
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'message': 'pong!'})  # Standardized response

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read', False)  # Default to False if not provided
        })
        return jsonify({'status': 'success', 'message': 'Book added!'}), 201  # HTTP 201 for created
    
    return jsonify({'status': 'success', 'books': BOOKS})  # GET response

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    if request.method == 'PUT':
        post_data = request.get_json()
        if not remove_book(book_id):
            return jsonify({'status': 'error', 'message': 'Book not found'}), 404
        BOOKS.append({
            'id': book_id,  # Preserve original ID
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read', False)
        })
        return jsonify({'status': 'success', 'message': 'Book updated!'})
    
    if request.method == 'DELETE':
        if not remove_book(book_id):
            return jsonify({'status': 'error', 'message': 'Book not found'}), 404
        return jsonify({'status': 'success', 'message': 'Book removed!'})

# Docker-required settings
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Must match docker-compose.yml