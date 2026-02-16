from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv

app = Flask(__name__)

@app.get("/")
def index():
    books = []
    with open("books.csv", mode="r", encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for book in csv_reader:
            books.append(book)

    return render_template("index.html", books=books)

@app.get("/add")
def show_add():
    return render_template("add-book.html")

@app.post("/add")
def add():
    with open("books.csv", mode="r", encoding='utf-8') as csv_file:
        csv_reader = list(csv.reader(csv_file))
        last_book = None
        last_id = 0

        if len(csv_reader) > 1:
            last_book = csv_reader[-1]

        if last_book:
            last_id = last_book[0]

        next_id = int(last_id) + 1    

    read_date = request.form.get("read_date")
    date_object = datetime.strptime(read_date, "%Y-%m-%d")
    formatted_date = date_object.strftime("%d/%m/%Y")

    new_book = [
        next_id,
        request.form.get("title"),
        request.form.get("writer"),
        request.form.get("cover_url"),
        request.form.get("stars"),
        formatted_date,
        request.form.get("review"),
    ]

    with open("books.csv", mode="a", encoding='utf-8', newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(new_book)

    return redirect(url_for("index"))

@app.get("/book/<int:book_id>")
def book_details(book_id):
    id_found = False
    book_found = None

    with open("books.csv", mode="r", encoding='utf-8') as csv_file: 
        csv_reader = csv.DictReader(csv_file)
        for book in csv_reader:
            if book_id == int(book['id']):
                id_found = True
                book_found = book
                break

    if id_found:
        return render_template("book-details.html", book=book_found)
    else:
        return "Livro não Encontrado!", 404
    


if (__name__) == "__main__":
    app.run(debug=True)
