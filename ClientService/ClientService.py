from queue import Empty
from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import requests
import json

ClientService=Blueprint('ClientService',__name__)

cache = {}
catalog1 = "http://catalog:5000"
oreder1 = "http://order:5000"

catalog2 = "http://catalog2:5000"
oreder2 = "http://order2:5000"

#load balancing alg round-robin
robin = False


#forward to catalog server-info
def get_books():
    global robin
    robin = not robin
    query =  requests.get((catalog1 if robin else catalog2)+"yyyyyyy/CATALOG_WEBSERVICE_IP/info")
    queryResponse = json.loads(query.text)
    return queryResponse

def get_book_by_id(id):
    global robin
    robin = not robin
    if(id not in cache):
        cache[id] = requests.get((catalog1 if robin else catalog2)+"/CATALOG_WEBSERVICE_IP/info/%s" % id).content
    print(cache)
    return cache[id]

    
def searchBookByTopic(topic):
    print(topic)
    global robin
    robin = not robin
    if (topic not in cache):
        cache[topic] = requests.get((catalog1 if robin else catalog2)+"/CATALOG_WEBSERVICE_IP/search/%s" % topic).content
    return cache[topic]

def purchase(id):
    global robin
    robin = not robin
    if (id in cache):
        cache.pop(id)
    requests.get((oreder1) + "/ORDER_WEBSERVICE_IP/purchase/%s" % id)
    return requests.get((oreder2)+"/ORDER_WEBSERVICE_IP/purchase/%s" % id).content

    
@ClientService.route("/Bazar/info")
def books_api():
    return jsonify(get_books()) 

@ClientService.route('/Bazar/info/<id>', methods=['GET'])
def get_api(id):
    return jsonify(get_book_by_id(id)) 

@ClientService.route("/Bazar/search/<topic>", methods=['GET'])
def topic_api(topic):
    return jsonify(searchBookByTopic(topic)) 

@ClientService.route('/Bazar/purchase/<id>')
def home_page(id):
    return purchase(id)