from database import Book, Borrower, add_books, add_borrowers
from mongoengine import *
from util import Item
from flask import render_template, make_response

default_db_name = 'app-yaotingj'

def reset_db():
    disconnect(alias="default")
    newdb_connection = connect(default_db_name)
    newdb_connection.drop_database(default_db_name)
    add_books()
    add_borrowers()
    return default_db_name + 'is connected'


def get_borrower_name(borrowerID):
    for borrower in Borrower.objects:
        if borrower.borrower_id == borrowerID:
            return borrower.name

def get_book_name(bookID):
    for book in Book.objects:
        if book.book_id == bookID:
            return book.title

def checkout_book(borrowerID, bookID):
    for b in Book.objects:
        if b.book_id == bookID and b.checked_out == "Y" and b.borrower_id != borrowerID:
            return get_book_name(bookID) + " is already checked out by someone"
        elif b.book_id == bookID and b.checked_out == "N" and b.borrower_id != borrowerID:
            b.checked_out = "Y"
            b.borrower_id=borrowerID
            b.borrower_name=get_borrower_name(borrowerID)
            b.save()
            return get_borrower_name(borrowerID) + ' has checked out ' + get_book_name(bookID)

def return_book(borrowerID, bookID):
    for b in Book.objects:
        if b.book_id == bookID and b.checked_out == "N" and b.borrower_id != borrowerID :
            return get_borrower_name(borrowerID) + ' has not currently checked out ' + get_book_name(bookID)
        elif b.book_id == bookID and b.checked_out == "Y" and b.borrower_id == borrowerID:
            b.checked_out = "N"
            b.borrower_id = ""
            b.borrower_name = ""
            b.save()
            return get_borrower_name(borrowerID) + ' has returned ' + get_book_name(bookID)

def get_books():
    book_list = []
    table_headers = ['book_id', 'title', 'author', 'checked_out', 'borrower_id', 'borrower_name']
    res_header = {'Content-Type': 'text/html'}

    for b in Book.objects:
        book_list.append(Item(b.book_id, b.title, b.author, b.checked_out, b.borrower_id, b.borrower_name))

    return make_response(render_template("index.html", headers=table_headers, objects=book_list), 200, res_header)