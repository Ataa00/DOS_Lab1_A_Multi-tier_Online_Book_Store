from flask import Flask,Blueprint
import ClientService 

app = Flask(__name__)

app.register_blueprint(ClientService.ClientService)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8786)