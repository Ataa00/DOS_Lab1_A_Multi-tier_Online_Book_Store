from flask import Flask,Blueprint
import ClientService 

app = Flask(__name__)

app.register_blueprint(ClientService.ClientService)


