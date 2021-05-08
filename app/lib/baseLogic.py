import configparser as conf
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
