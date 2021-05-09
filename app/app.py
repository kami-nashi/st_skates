from flask import Flask
from flask import request, jsonify
import json
import configparser as conf
import lib.baseLogic as base

app = Flask(__name__)
appConfig = base.baseConfig()
app.config['SECRET_KEY'] = appConfig

@app.route('/', methods=['GET'])
def home():
    return "<h1>Your destination is not here ... </p>"

@app.route('/api/v1/resources/skates/master/<int:uSkaterUUID>', methods=['GET'])
def api_master(uSkaterUUID):
    skates = base.buildMasterResponse(uSkaterUUID)
    return skates

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5021, use_reloader=True, debug=True)
