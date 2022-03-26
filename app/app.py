from flask import Flask, request, jsonify
import st_dbConf
import lib.baseLogic as base

app = Flask(__name__)
appConfig = st_dbConf.baseConfig()
app.config['SECRET_KEY'] = appConfig


@app.route('/', methods=['GET'])
def home():
    return "<h1>Your destination is not here ... </p>"


@app.route('/api/v1/resources/skates/master/<int:uSkaterUUID>', methods=['GET'])
def api_master(uSkaterUUID):
    skates = base.buildMasterResponse(uSkaterUUID)
    return skates


@app.route('/api/v1/resources/skates/active/<int:uSkaterUUID>', methods=['GET'])
def api_active(uSkaterUUID):
    skates = base.buildActiveResponse(uSkaterUUID)
    return jsonify(skates)


@app.route('/api/v1/resources/skates/list/<int:uSkaterUUID>', methods=['GET'])
def api_list(uSkaterUUID):
    skates = base.buildListResponse(uSkaterUUID)
    return jsonify(skates)


@app.route('/api/v1/resources/skates/listHours/<int:uSkaterUUID>', methods=['GET'])
def api_listHours(uSkaterUUID):
    listSkatesHours = base.SkatesListHoursPerConfig(uSkaterUUID)
    return jsonify(listSkatesHours)


@app.route('/api/v1/resources/skates/listBoots/<int:uSkaterUUID>', methods=['GET'])
def api_listBoots(uSkaterUUID):
    skates = base.skaterListBoots(uSkaterUUID)
    return jsonify(skates)


@app.route('/api/v1/resources/skates/listBlades/<int:uSkaterUUID>', methods=['GET'])
def api_listBlades(uSkaterUUID):
    skates = base.skaterListBlades(uSkaterUUID)
    return jsonify(skates)


@app.route('/api/v1/resources/skates/createSkates', methods=['POST', 'GET'])
def createSkates():
    dataSkaterID = request.form.get('uSkaterUUID')
    dataBoots = request.form.get('boots')
    dataBlades = request.form.get('blades')
    data = (dataSkaterID, dataBlades, dataBoots)
    base.addNewSkates(data)
    return str(data)


@app.route('/api/v1/resources/skates/createBoots', methods=['POST'])
def createBoots():
    request_data = request.get_json()
    results = base.addNewBoots(request_data)
    return results


@app.route('/api/v1/resources/skates/createBlades', methods=['POST'])
def createBlades():
    request_data = request.get_json()
    results = base.addNewBlades(request_data)
    return results


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5021, use_reloader=True, debug=True)
