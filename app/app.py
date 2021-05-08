from flask import Flask
from flask import request, jsonify
import configparser as conf
import lib.baseLogic as base

app = Flask(__name__)
appConfig = base.baseConfig()
app.config['SECRET_KEY'] = appConfig

@app.route('/', methods=['GET'])
def home():
    return "<h1>Look</p>"

skatesActive = base.skaterActiveMeta(1)
skatesList = base.skaterListSkates(1)

skates = {'active': skatesActive, 'list': skatesList}

@app.route('/api/v1/resources/skates/master', methods=['GET'])
def api_master():
    return jsonify(skates)

@app.route('/api/v1/resources/skates/active', methods=['GET'])
def api_active():
    return jsonify(skatesActive)

@app.route('/api/v1/resources/skates/list', methods=['GET'])
def api_list():
    return jsonify(skatesList)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5021, use_reloader=True, debug=True)
