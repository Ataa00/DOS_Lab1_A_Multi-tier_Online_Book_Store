from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3
import requests
import json
import os

catalog1 = "http://catalog:5000"

catalog2 = "http://catalog2:5000"

#load balancing alg round-robin
robin = False


order=Blueprint('order',__name__)

def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 

def purchase(id):
    global robin
    robin = not robin
    if robin:
        ip = catalog1+"/CATALOG_WEBSERVICE_IP/findBook/"
        
    else:
        ip = catalog2+"/CATALOG_WEBSERVICE_IP/findBook/"
        
    
    print(ip)
    ip = ip + id
    query = requests.get(ip)
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

        ip = catalog1+"/CATALOG_WEBSERVICE_IP/update/"
        ip2 = catalog2+"/CATALOG_WEBSERVICE_IP/update/"
            
        print(ip)
        ip = ip + str(id)
        ip2 = ip2 + str(id)

        Update = requests.put(ip, json=request).text
        Update2 = requests.put(ip2, json=request).text

        response = {}
        response["BeforePurchased"] =  book
        response["AfterPurchased"] = json.loads(Update)
        if response["AfterPurchased"]["status"] == "OK":
            return response
        else:
            return {"book":book,"Message":"There is no enough books in the storage."}
    else:
        return {"msg":"There is no book with this ID"}

@order.route('/ORDER_WEBSERVICE_IP/purchase/<id>')
def home_page(id):
    return purchase(id)