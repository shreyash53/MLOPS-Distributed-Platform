from dbconfig import *

db = mongodb()

class Book(db.Document):
    book_id = db.IntField()
    name = db.StringField()
    author = db.StringField()

    def to_json(self):
        return {
            "book_id":self.book_id,
            "name": self.name,
            "author":self.author
        }

print("\nCreate a Book")
book = Book(book_id=2,
name = "Harry Potter",
author = "J.K. Rowling"
)

book.save()

print("\nFetch a book")
book = Book.objects(book_id=2).first()
print(book.to_json())