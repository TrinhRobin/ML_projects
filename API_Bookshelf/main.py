from fastapi import FastAPI
from book import Book, damerau_levenshtein_distance
import pandas as pd

app = FastAPI()
books_db = pd.read_csv('books.csv')

@app.post("/books/")
async def create_book(book: Book):
    global books_db
    books_db = books_db.append(book.dict(), ignore_index=True)
    return {"message": "Livre ajouté avec succès !"}


@app.get("/books/")
async def get_books():
    global books_db
    return  books_db.sample(n=1).fillna('').to_dict(orient="records")


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    global books_db
    if 0 <= book_id < len(books_db):
        return books_db.iloc[book_id].fillna(' ').to_dict()
    return {"error": "Livre non trouvé"}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    global books_db
    if 0 <= book_id < len(books_db):
        deleted_book = books_db.iloc[book_id].to_dict()
        books_db = books_db.drop(index=book_id).reset_index(drop=True)
        return {"message": f"Livre '{deleted_book['title']}' supprimé avec succès !"}
    return {"error": "Livre non trouvé"}

@app.get("/search/")
async def search_books(query: str):
    global books_db
    # Recherche le livre le plus proche en utilisant Damerau-Levenshtein distance
    closest_title = min(books_db['Title'], key=lambda x: damerau_levenshtein_distance(query, x))
    closest_book = books_db[books_db['Title'] == closest_title].iloc[0].to_dict()
    return {'answer' : closest_book, 'title': closest_title}