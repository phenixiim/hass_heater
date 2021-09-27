entity = "switch.kotel"
maxDiffToRunEngine = -0.5
blockIntervalInSeconds = 60*10

sensorList = {
        "obyvak" : "climate.bfc4b12743d95bf5b1paaj",
        "koupelna" : "climate.bfc2943d4e885e44afarml",
        "kubik" : "climate.bfce8fac3c330bbc7cb8cl",
        "marketka" : "climate.bf255f1dfba3639cb6rbda",
        "loznice" : "climate.bfd99da354381754cdsk6r",
        "koupelna" : "climate.bfc2943d4e885e44afarml",
        "zimni_zahrada" : "climate.bfb62e94aeeeebd6075hp7"
}

def getCurrentState():
	return hass.states.get(entity).state

def engineOn():
	if (getCurrentState() == 'on'):
		logger.info("nothing to do, already switched on")
		return None
	logger.info("switching engine on")
	hass.services.call("switch","turn_on",{"entity_id": entity})

def engineOff():
	if (getCurrentState() == 'off'):
                logger.info("nothing to do, already switched off")
                return None
	logger.info("switching engine off")
	hass.services.call("switch","turn_off",{"entity_id": entity})

def getCurrentTemperature(entity):
	return hass.states.get(entity).attributes["current_temperature"]

def getTemperature(entity):
        return hass.states.get(entity).attributes["temperature"]

def getTemperatureDiff(entity):
	return (getCurrentTemperature(entity)-getTemperature(entity))

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
	engineOff()

runDecisionEngine()
