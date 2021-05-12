import configparser as conf
from flask import jsonify
import pymysql

def baseConfig():
    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    appConfig = configParser.get('appKey', 'secret')
    return appConfig

def dbconnect(sql,vTUP=None):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)

   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')

   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
   cur = con.cursor()
   cur.execute(sql, vTUP)
   tables = cur.fetchall()
   cur.connection.commit()
   con.close()
   return tables

def skaterListBlades(uSkaterUUID):
    q = '''
    select fsBlades.bladesName, fsBlades.bladesModel, fsBlades.bladesSize, fsBlades.bladesPurchAmount, DATE_FORMAT(fsBlades.bladesPurchDate, "%%Y-%%m-%%d") as bladesDate, sConfig.aSkateConfigID
    from uSkateConfig sConfig
    INNER JOIN uSkaterBlades fsBlades ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID and sConfig.uSkaterBladesID = fsBlades.bladeID
	INNER JOIN uSkaterConfig fsConfig ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    '''
    results = dbconnect(q,uSkaterUUID)
    return results

def skaterListBoots(uSkaterUUID):
    q = '''
    select fsBoots.bootsName, fsBoots.bootsModel, fsBoots.bootsSize, fsBoots.bootsPurchAmount, DATE_FORMAT(fsBoots.bootsPurchDate, "%%Y-%%m-%%d") as bootsDate, sConfig.aSkateConfigID
    from uSkateConfig sConfig
    INNER JOIN uSkaterBoots fsBoots ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID and sConfig.uSkaterBootsID = fsBoots.bootID
	INNER JOIN uSkaterConfig fsConfig ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    '''
    results = dbconnect(q,uSkaterUUID)
    return results

def skaterListSkates(uSkaterUUID):
    q = '''
    select fsBoots.bootsName, fsBoots.bootsModel, fsBlades.bladesName, fsBlades.bladesModel, sConfig.aSkateConfigID
    from uSkateConfig sConfig
    INNER JOIN uSkaterBoots fsBoots ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID and sConfig.uSkaterBootsID = fsBoots.bootID
    INNER JOIN uSkaterBlades fsBlades ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID and sConfig.uSkaterBladesID = fsBlades.bladeID
    where sConfig.uSkaterUUID = %s
    '''
    results = dbconnect(q,uSkaterUUID)
    return results

def skaterActiveHours(uSkaterUUID):
    q = '''
    SELECT ifnull(sum(ice_time.ice_time/60),0) as tHours from ice_time,(
	  select sConfig.uSkaterUUID, fsBoots.bootsName, fsBoots.bootsModel, fsBlades.bladesName, fsBlades.bladesModel, sConfig.aSkateConfigID
      from uSkateConfig sConfig
      INNER JOIN uSkaterBoots fsBoots ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID and sConfig.uSkaterBootsID = fsBoots.bootID
      INNER JOIN uSkaterBlades fsBlades ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID and sConfig.uSkaterBladesID = fsBlades.bladeID
	  INNER JOIN uSkaterConfig fsConfig ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
      WHERE sConfig.uSkaterUUID = %s
      AND sConfig.aSkateConfigID = fsConfig.uSkateComboIce
    ) actSkate
    WHERE ice_time.uSkaterUUID = actSkate.uSkaterUUID and ice_time.uSkaterConfig = actSkate.aSkateConfigID
    '''
    results = dbconnect(q,uSkaterUUID)
    return results

def skaterActiveMeta(uSkaterUUID):
    q = '''
    select fsBoots.bootsName, fsBoots.bootsModel, fsBlades.bladesName, fsBlades.bladesModel, sConfig.aSkateConfigID
    from uSkateConfig sConfig
    INNER JOIN uSkaterBoots fsBoots ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID and sConfig.uSkaterBootsID = fsBoots.bootID
    INNER JOIN uSkaterBlades fsBlades ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID and sConfig.uSkaterBladesID = fsBlades.bladeID
	INNER JOIN uSkaterConfig fsConfig ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    AND sConfig.aSkateConfigID = fsConfig.uSkateComboIce
    '''
    results = dbconnect(q,uSkaterUUID)
    return results

def skaterListHours(uSkaterUUID):
    ConfigID = skaterActiveHours(uSkaterUUID)
    vTup(uSkaterUUID,ConfigID)
    q = '''
    select fsBoots.bootsName, fsBoots.bootsModel, fsBlades.bladesName, fsBlades.bladesModel, sConfig.aSkateConfigID
    from uSkateConfig sConfig
    INNER JOIN uSkaterBoots fsBoots ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID and sConfig.uSkaterBootsID = fsBoots.bootID
    INNER JOIN uSkaterBlades fsBlades ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID and sConfig.uSkaterBladesID = fsBlades.bladeID
	INNER JOIN uSkaterConfig fsConfig ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    AND sConfig.aSkateConfigID = %s
    '''
    results = dbconnect(q,uSkaterUUID)
    return results

def buildMasterResponse(uSkaterUUID):
    skatesActive = skaterActiveMeta(uSkaterUUID)
    skatesList = skaterListSkates(uSkaterUUID)
    skatesBoots = skaterListBoots(uSkaterUUID)
    skatesBlades = skaterListBlades(uSkaterUUID)
    skates = {'active': skatesActive, 'list': skatesList, 'skatesBoots': skatesBoots, 'skatesBlades': skatesBlades}
    return jsonify(skates)

def buildActiveResponse(uSkaterUUID):
    skatesActive = skaterActiveMeta(uSkaterUUID)
    return skatesActive

def buildListResponse(uSkaterUUID):
    skatesList = skaterListSkates(uSkaterUUID)
    return skatesList

def buildMasterResponseTest(uSkaterUUID):
    #skatesActive = skaterActiveMeta(uSkaterUUID)
    #skatesList = skaterListSkates(uSkaterUUID)
    #skatesBoots = skaterListBoots(uSkaterUUID)
    #skatesBlades = skaterListBlades(uSkaterUUID)
    #skates = {'active': skatesActive, 'list': skatesList, 'skatesBoots': skatesBoots, 'skatesBlades': skatesBlades}
    skatesActive = skaterActiveMeta(uSkaterUUID)
    print(jsonify({'active':skatesActive}))
    return jsonify({'active':skatesActive})

def addNewBoots(request_data):
    uSkaterUUID = request_data['uSkaterUUID']

    if len(request_data['bootsName']) == 0:
        bootsName = 'Generic'
    else:
        bootsName = request_data['bootsName']

    if len(request_data['bootsModel']) == 0:
        bootsModel = 'Generic'
    else:
        bootsModel = request_data['bootsModel']

    if len(request_data['bootsSize']) == 0:
        bootsSize = '0'
    else:
        bootsSize = request_data['bootsSize']

    if len(request_data['bootsPurchDate']) == 0:
        bootsPurchDate = '0000-00-00'
    else:
        bootsPurchDate = request_data['bootsPurchDate']

    if len(request_data['bootsPurchAmount']) == 0:
        bootsPurchAmount = float(0.0)
    else:
        bootsPurchAmount = request_data['bootsPurchAmount']

    bootsTuple = (bootsName, bootsModel, bootsSize, bootsPurchDate, bootsPurchAmount, uSkaterUUID)
    bootsQuery = "INSERT INTO uSkaterBoots (bootsName, bootsModel, bootsSize, bootsPurchDate, bootsPurchAmount, uSkaterUUID, bootID) select %s, %s, %s, %s, %s, %s, max(bootID)+1 from uSkaterBoots;"
    results = dbconnect(bootsQuery,bootsTuple)

    # nice diagnostic check here
    #results = '''{} {} boots, size {}, bought on {} for ${}'''.format(bootsName, bootsModel, bootsSize, bootsPurchDate, bootsPurchAmount)
    #print(results)
    return str(200)

def addNewBlades(request_data):
    uSkaterUUID = request_data['uSkaterUUID']

    if len(request_data['bladesName']) == 0:
        bladesName = 'Generic'
    else:
        bladesName = request_data['bladesName']

    if len(request_data['bladesModel']) == 0:
        bladesModel = 'Generic'
    else:
        bladesModel = request_data['bladesModel']

    if len(request_data['bladesSize']) == 0:
        bladesSize = '0'
    else:
        bladesSize = request_data['bladesSize']

    if len(request_data['bladesPurchDate']) == 0:
        bladesPurchDate = '0000-00-00'
    else:
        bladesPurchDate = request_data['bladesPurchDate']

    if len(request_data['bladesPurchAmount']) == 0:
        bladesPurchAmount = float(0.0)
    else:
        bladesPurchAmount = request_data['bladesPurchAmount']

    bladesTuple = (bladesName, bladesModel, bladesSize, bladesPurchDate, bladesPurchAmount, uSkaterUUID)
    bladesQuery = "INSERT INTO uSkaterBlades (bladesName, bladesModel, bladesSize, bladesPurchDate, bladesPurchAmount, uSkaterUUID, bladeID) select %s, %s, %s, %s, %s, %s, max(bladeID)+1 from uSkaterBlades;"
    results = dbconnect(bladesQuery,bladesTuple)
    return str(200)
