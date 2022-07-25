from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3
import requests
import json

order=Blueprint('order',__name__)

def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 

def purchase(id):
    query = requests.get(f"http://127.0.0.1:8787/CATALOG_WEBSERVICE_IP/findBook/{id}")
    
    id = int(id)
    
    queryResponse = json.loads(query.text)
    print(queryResponse)
    flag = False
    
    if queryResponse["status"] == "NO":
        return {"status": "There is no book with this ID"}

    book = queryResponse["beforePurchased"]

    print(book)

    if book["id"] == id:
        flag = True

    if flag:
        request = {
            "book":book
        }
        Update = requests.put(f"http://127.0.0.1:8787/CATALOG_WEBSERVICE_IP/update/{id}", json=request)
        response = {}
        response["BeforePurchased"] =  book
        response["AfterPurchased"] = json.loads(Update.text)
        if response["AfterPurchased"]["status"] == "OK":
            return response
        else:
            return {"book":book,"Message":"There is no enough books in the storage."}
    else:
        return "There is no book with this ID"

@order.route('/ORDER_WEBSERVICE_IP/purchase/<id>')
def home_page(id):
    return purchase(id)