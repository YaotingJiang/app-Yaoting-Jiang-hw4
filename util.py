class Item(object):
    def __init__(self, book_id, title, author, checked_out, borrower_id, borrower_name):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.checked_out = checked_out
        self.borrower_id = borrower_id
        self.borrower_name = borrower_name