from flask import Flask
from flask_restful import Api, Resource, reqparse
from main import get_books, reset_db, checkout_book, return_book
from database import Book, Borrower

app = Flask(__name__)
api = Api(app)

@app.route('/')
def entry():
    return 'Please enter a command through the url'

class books_resource(Resource):
    def get(self):
        res = get_books()
        return res

class reset_resources(Resource):
    def get(self):
        res = reset_db()
        return res

class checkout_resource(Resource):
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('borrowerId', type=str)
        get_parser.add_argument('bookId', type=str)
        args = get_parser.parse_args()

        is_bookid_valid = any(book.book_id == args.bookId for book in Book.objects)
        is_borrowerid_valid = any(borrower.borrower_id == args.borrowerId for borrower in Borrower.objects)

        if not is_bookid_valid:
            return 'Book with ID ' + args.bookId + ' does not exist'
        elif not is_borrowerid_valid:
            return 'Borrower with ID ' + args.borrowerId + ' does not exist'
        else:
            return checkout_book(args.borrowerId, args.bookId)


class return_resource(Resource):
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('borrowerId', type=str)
        get_parser.add_argument('bookId', type=str)
        args = get_parser.parse_args()

        is_bookid_valid = any(book.book_id == args.bookId for book in Book.objects)
        is_borrowerid_valid = any(borrower.borrower_id == args.borrowerId for borrower in Borrower.objects)

        if not is_bookid_valid:
            return 'Book with ID ' + args.bookId + ' does not exist'
        elif not is_borrowerid_valid:
            return 'Borrower with ID ' + args.borrowerId + ' does not exist'
        else:
            return return_book(args.borrowerId, args.bookId)


api.add_resource(books_resource, '/books')
api.add_resource(reset_resources, '/reset')
api.add_resource(checkout_resource, '/checkout')
api.add_resource(return_resource, '/return')

if __name__ == "__main__":
    app.run()