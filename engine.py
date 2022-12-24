entity = "switch.kotel"
maxDiffToRunEngine = -0.5
blockIntervalInSeconds =60

sensorList = {
	"obyvak" : "climate.obyvak1",
	"kubik" : "climate.kubik",
	"marketka" : "climate.marketka",
	"loznice" : "climate.loznice",
	"zimni_zahrada" : "climate.zimni_zahrada"
}

def getEngineCurrentState():
	return hass.states.get(entity).state

def engineOn():
	logger.info("switching engine on")
	hass.services.call("switch","turn_on",{"entity_id": entity})

def engineOff():
	logger.info("switching engine off")
	hass.services.call("switch","turn_off",{"entity_id": entity})

def getCurrentTemperature(entity):
	return hass.states.get(entity).attributes["current_temperature"]

def getDesiredTemperature(entity):
        return hass.states.get(entity).attributes["temperature"]

def getTemperatureDiff(entity):
	return (getCurrentTemperature(entity)-getDesiredTemperature(entity))

def isDecisionEngineBlocked():
	lastChange = hass.states.get(entity).last_changed.timestamp()
	now = datetime.datetime.now().timestamp()
	lastChangeInSeconds = (lastChange - now)
	if lastChangeInSeconds < -1*blockIntervalInSeconds:
		return False
	return True

def runDecisionEngine():
    if isDecisionEngineBlocked():
        logger.info("decession engine blocked, ending...")
        return None
    logger.info("starting decession engine for heating....")
    for sensorKey in sensorList:
        currentDiff = getTemperatureDiff(sensorList[sensorKey])
        if (currentDiff < maxDiffToRunEngine):
            logger.info("sensor '%s' out of tolerance diff limit (%s), starting engine...",sensorKey,currentDiff)
            return engineOn()

    logger.info("all diffs in tolerance limits, no heating needed...")

    return engineOff()

def runDecisionEngineWithHysteresis():
    if isDecisionEngineBlocked():
        logger.info("decession engine blocked, ending...")
        return None
    logger.info("starting decession engine for heating....")

    finalDiff = maxDiffToRunEngine
    if (getEngineCurrentState() == "on"):
        logger.info("engine on, inverting the diff limit")
        finalDiff = -1 * maxDiffToRunEngine
    for sensorKey in sensorList:
        currentDiff = getTemperatureDiff(sensorList[sensorKey])
        if (currentDiff <= finalDiff):
            logger.info("sensor '%s' out of tolerance diff limit (%s), starting engine...",sensorKey,currentDiff)
            return engineOn()

    logger.info("all diffs in tolerance limits, no heating needed...")

    return engineOff()

#runDecisionEngine()
runDecisionEngineWithHysteresis()
