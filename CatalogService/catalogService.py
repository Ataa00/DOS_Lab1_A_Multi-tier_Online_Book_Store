from email.message import Message
from queue import Empty
from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3 

catalogService=Blueprint('catalogService',__name__)

#Data base Connection
def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 

#Get all books from the DB.
def get_books():
    books = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM book")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            book = {}
            # book["id"] = i["id"]
            book["title"] = i["title"]
            # book["topic"] = i["topic"]
            book["quantity"] = i["quantity"]
            book["price"] = i["price"]
            books.append(book)
        conn.close()     

    except Exception as e:
        print(e)
        books = ["error to get books"]

    return books

#Get a specifice Book from its ID.
def get_book_by_id(id):
    book = {}
    try:
        conn = connect_to_db()
        
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT title,quantity,price FROM book WHERE id = ?",(id))
        row = cur.fetchone()
        # convert row object to dictionary
        print(row)
        if row is None:
            return {"status":f"There is No book has id = {id}"}
        book["title"] = row["title"]
        book["quantity"] = row["quantity"]
        book["price"] = row["price"]
        conn.close()
    except Exception as e:
        print(e)
        book = {"error to get book"}
         
    return book

#Search for a book by its topic
def searchBookByTopic(topic):
    books = []
    print(topic)
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM book WHERE topic=?",[topic])
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            book = {}
            book["id"] = i["id"]
            book["title"] = i["title"]
            books.append(book)
        conn.close()
    except Exception as e:
        print(e)
        return {"status":"error to get books"}

    if books == []:
        return {"status":f"There is no books with this topic {topic}"}

    return books  

#To Find if there is a book in the stoke. For Order Query......
def findBook(id):
    response = {}
    book = {}
    try:
        conn = connect_to_db()
        
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT title,quantity,price,id FROM book WHERE id = ?",(id))
        row = cur.fetchone()
        # convert row object to dictionary
        
        if row is None:
            return {"status":"NO"}
        book["title"] = row["title"]
        book["quantity"] = row["quantity"]
        book["price"] = row["price"]
        book["id"] = row["id"]
        response["beforePurchased"] = book
        conn.close()
    except Exception as e:
        print(e)
        response = {"error to get book"}
    response["status"] = "YES"    
    return response

#To update Books price or quantity or both
def update_book(id, book):
    updated_book = {}
    if book["quantity"] < 1:
        updated_book = {"status":"NO", "Message":"There is no enogh book in the store."}
        print(updated_book)
        return updated_book
    else:
        updated_book = {"status":"OK"}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE book SET quantity = ? WHERE id =?",  
                     (book["quantity"]-1,  id,))
        conn.commit()
        #return the user
        updated_book["Item"] = get_book_by_id(id)
        

    except:
        return {"status":f"There is no book with id = {book['id']}"}
    finally:
        conn.close()

    print(updated_book)

    return updated_book

@catalogService.route("/CATALOG_WEBSERVICE_IP/info")
def books_api():
    return jsonify(get_books()) 

@catalogService.route('/CATALOG_WEBSERVICE_IP/info/<id>', methods=['GET'])
def get_api(id):
    return jsonify(get_book_by_id(id)) 

@catalogService.route("/CATALOG_WEBSERVICE_IP/search/<topic>", methods=['GET'])
def topic_api(topic):
    return jsonify(searchBookByTopic(topic)) 

@catalogService.route('/CATALOG_WEBSERVICE_IP/findBook/<id>', methods=['GET'])
def findBook_api(id):
    return jsonify(findBook(id))

@catalogService.route('/CATALOG_WEBSERVICE_IP/update/<id>', methods=['PUT'])
def update_api(id):
    response = request.get_json()
    return jsonify(update_book(id, response["book"]))