from flask import jsonify
import st_dbConf


def skaterListBlades(uSkaterUUID):
    q = '''
    SELECT
        fsBlades.bladesName,
        fsBlades.bladesModel,
        fsBlades.bladesSize,
        fsBlades.bladesPurchAmount,
        DATE_FORMAT(fsBlades.bladesPurchDate, "%%Y-%%m-%%d") as bladesDate,
        sConfig.aSkateConfigID
    FROM uSkateConfig sConfig
        INNER JOIN uSkaterBlades fsBlades
        ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID
        AND sConfig.uSkaterBladesID = fsBlades.bladeID
        INNER JOIN uSkaterConfig fsConfig
        ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    '''
    results = st_dbConf.dbconnect(q, uSkaterUUID)
    return results


def skaterListBoots(uSkaterUUID):
    q = '''
    SELECT DISTINCT 
        fsBoots.bootsName,
        fsBoots.bootsModel,
        fsBoots.bootsSize,
        fsBoots.bootsPurchAmount,
        DATE_FORMAT(fsBoots.bootsPurchDate, "%%Y-%%m-%%d") as bootsDate
    from uSkateConfig sConfig
        INNER JOIN uSkaterBoots fsBoots
        ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID
        AND sConfig.uSkaterBootsID = fsBoots.bootID
        INNER JOIN uSkaterConfig fsConfig
        ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    '''
    results = st_dbConf.dbconnect(q, uSkaterUUID)
    return results


def skaterListSkates(uSkaterUUID):
    q = '''
    select
        fsBoots.bootsName,
        fsBoots.bootsModel,
        fsBlades.bladesName,
        fsBlades.bladesModel,
        sConfig.aSkateConfigID,
        sum(iTime.ice_time) / 60 as aSkateConfigTime
    from
        uSkateConfig sConfig
        INNER JOIN uSkaterBoots fsBoots
        ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID
        and sConfig.uSkaterBootsID = fsBoots.bootID
        INNER JOIN uSkaterBlades fsBlades
        ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID
        and sConfig.uSkaterBladesID = fsBlades.bladeID
        INNER JOIN ice_time iTime
        ON sConfig.uSkaterUUID = iTime.uSkaterUUID
        and sConfig.aSkateConfigID = iTime.uSkaterConfig
    WHERE
        sConfig.uSkaterUUID = %s
    GROUP BY
        sConfig.aSkateConfigID
    '''
    results = st_dbConf.dbconnect(q, uSkaterUUID)
    return results


def skaterActiveHours(uSkaterUUID):
    q = '''
    SELECT
        ifnull(sum(ice_time.ice_time/60),0) as tHours from ice_time,(
            SELECT
            sConfig.uSkaterUUID,
            fsBoots.bootsName,
            fsBoots.bootsModel,
            fsBlades.bladesName,
            fsBlades.bladesModel,
            sConfig.aSkateConfigID
        FROM uSkateConfig sConfig
            INNER JOIN uSkaterBoots fsBoots
            ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID
            and sConfig.uSkaterBootsID = fsBoots.bootID
            INNER JOIN uSkaterBlades fsBlades
            ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID
            and sConfig.uSkaterBladesID = fsBlades.bladeID
            INNER JOIN uSkaterConfig fsConfig
            ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
        WHERE sConfig.uSkaterUUID = %s
        AND sConfig.aSkateConfigID = fsConfig.uSkateComboIce
        ) actSkate
    WHERE ice_time.uSkaterUUID = actSkate.uSkaterUUID
    and ice_time.uSkaterConfig = actSkate.aSkateConfigID
    '''
    results = st_dbConf.dbconnect(q, uSkaterUUID)
    return results


def skaterActiveMeta(uSkaterUUID):
    q = '''
    SELECT
        fsBoots.bootsName,
        fsBoots.bootsModel,
        fsBlades.bladesName,
        fsBlades.bladesModel,
        sConfig.aSkateConfigID
    FROM uSkateConfig sConfig
        INNER JOIN uSkaterBoots fsBoots
        ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID
        and sConfig.uSkaterBootsID = fsBoots.bootID
        INNER JOIN uSkaterBlades fsBlades
        ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID
        and sConfig.uSkaterBladesID = fsBlades.bladeID
        INNER JOIN uSkaterConfig fsConfig
        ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    AND sConfig.aSkateConfigID = fsConfig.uSkateComboIce
    '''
    results = st_dbConf.dbconnect(q, uSkaterUUID)
    return results


def skaterListHours(uSkaterUUID):
    q = '''
    SELECT
        fsBoots.bootsName,
        fsBoots.bootsModel,
        fsBlades.bladesName,
        fsBlades.bladesModel,
        sConfig.aSkateConfigID
    from uSkateConfig sConfig
        INNER JOIN uSkaterBoots fsBoots
        ON sConfig.uSkaterUUID = fsBoots.uSkaterUUID
        and sConfig.uSkaterBootsID = fsBoots.bootID
        INNER JOIN uSkaterBlades fsBlades
        ON sConfig.uSkaterUUID = fsBlades.uSkaterUUID
        and sConfig.uSkaterBladesID = fsBlades.bladeID
        INNER JOIN uSkaterConfig fsConfig
        ON sConfig.uSkaterUUID = fsConfig.uSkaterUUID
    WHERE sConfig.uSkaterUUID = %s
    AND sConfig.aSkateConfigID = %s
    '''
    results = st_dbConf.dbconnect(q, uSkaterUUID)
    return results


def SkatesListHoursPerConfig(uSkaterUUID):
    q = '''
    SELECT
        uSkaterConfig,
        SUM(ice_time.ice_time/60) as configHours
    FROM uSkateConfig, ice_time
    WHERE ice_time.uSkaterUUID = %s
    and uSkateConfig.aSkateConfigID = ice_time.uSkaterConfig
    GROUP BY ice_time.uSkaterConfig
    '''
    results = st_dbConf.dbconnect(q, uSkaterUUID)
    return results


def buildMasterResponse(uSkaterUUID):
    skatesActive = skaterActiveMeta(uSkaterUUID)
    skatesList = skaterListSkates(uSkaterUUID)
    skatesBoots = skaterListBoots(uSkaterUUID)
    skatesBlades = skaterListBlades(uSkaterUUID)
    skates = {'active': skatesActive, 'list': skatesList,
              'skatesBoots': skatesBoots, 'skatesBlades': skatesBlades}
    return jsonify(skates)


def buildActiveResponse(uSkaterUUID):
    skatesActive = skaterActiveMeta(uSkaterUUID)
    return skatesActive


def buildListResponse(uSkaterUUID):
    skatesList = skaterListSkates(uSkaterUUID)
    return skatesList


def buildMasterResponseTest(uSkaterUUID):
    # skatesActive = skaterActiveMeta(uSkaterUUID)
    # skatesList = skaterListSkates(uSkaterUUID)
    # skatesBoots = skaterListBoots(uSkaterUUID)
    # skatesBlades = skaterListBlades(uSkaterUUID)
    # skates = {'active': skatesActive, 'list': skatesList,
    #           'skatesBoots': skatesBoots, 'skatesBlades': skatesBlades}
    skatesActive = skaterActiveMeta(uSkaterUUID)
    print(jsonify({'active': skatesActive}))
    return jsonify({'active': skatesActive})


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

    bootsTuple = (bootsName, bootsModel, bootsSize,
                  bootsPurchDate, bootsPurchAmount, uSkaterUUID)
    bootsQuery = '''
    INSERT INTO uSkaterBoots (
        bootsName,
        bootsModel,
        bootsSize,
        bootsPurchDate,
        bootsPurchAmount,
        uSkaterUUID,
        bootID
        )
    SELECT %s, %s, %s, %s, %s, %s, max(bootID)+1 from uSkaterBoots;
    '''
    # results = st_dbConf.dbconnect(bootsQuery, bootsTuple)

    # nice diagnostic check here
    #
    # results = '''{} {} boots, size {}, bought on {} for ${}'''.format(
    #    bootsName, bootsModel, bootsSize, bootsPurchDate, bootsPurchAmount)
    # print(results)
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

    bladesTuple = (bladesName, bladesModel, bladesSize,
                   bladesPurchDate, bladesPurchAmount, uSkaterUUID)
    bladesQuery = '''
    INSERT INTO uSkaterBlades (
        bladesName,
        bladesModel,
        bladesSize,
        bladesPurchDate,
        bladesPurchAmount,
        uSkaterUUID,
        bladeID
        )
    SELECT %s, %s, %s, %s, %s, %s, max(bladeID)+1
    FROM uSkaterBlades;
    '''
    results = st_dbConf.dbconnect(bladesQuery, bladesTuple)
    return str(200)


def addNewSkates(request_data):
    print(request_data)
    skatesQuery = "INSERT INTO uSkateConfig (uSkaterUUID, uSkaterBladesID, uSkaterBootsID, sType, sActive, aSkateConfigID) select %s, %s, %s, 1, 1, max(aSkateConfigID)+1 from uSkateConfig;"
    results = st_dbConf.dbconnect(skatesQuery, request_data)
    return str(200)
