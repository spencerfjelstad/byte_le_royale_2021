extends Node2D


# Rock starting place = 680, 400
var turn = 1
var restart = false
var turns = []
var data = {}

var eventsDict = {
	"ice": {
		"active": false,
		"originx": 600,
		"originy": 425,
		"destx": 600,
		"desty": 800,
		},
	"rock": false
}

var body_sprites = ["res://assets/upgrades/upgrades_body_headlights.png","res://assets/upgrades/upgrades_body_sentry.png","res://assets/upgrades/upgrades_body_tank.png"]
var tires_sprites = ["res://assets/upgrades/upgrades_tires_economy.png","res://assets/upgrades/upgrades_tires_monster.png","res://assets/upgrades/upgrades_tires_normal.png","res://assets/upgrades/upgrades_tires_sticky.png"]
var addons_sprites = ["res://assets/upgrades/upgrades_addons_GPS.png","res://assets/upgrades/upgrades_addons_policescanner.png","res://assets/upgrades/upgrades_addons_rabbit_foot.png",]

func _ready():
	var file = File.new()
	file.open("../../logs/turn_logs.json", file.READ)
	var text = file.get_as_text()
	var result_json = JSON.parse(text)
	file.close()
	
	if result_json.error == OK:
		data = result_json.result
	
	
	
	var viewportWidth = get_viewport().size.x
	var viewportHeight = get_viewport().size.y

	var scale = viewportWidth / $TruckHUD.texture.get_size().x

	# Optional: Center the sprite, required only if the sprite's Offset>Centered checkbox is set
	$TruckHUD.set_position(Vector2(viewportWidth/2, viewportHeight/2))

	# Set same scale value horizontally/vertically to maintain aspect ratio
	# If however you don't want to maintain aspect ratio, simply set different
	# scale along x and y
	$TruckHUD.set_scale(Vector2(scale, scale))
	
	
	
	
	
	
	$Timer.set_wait_time(1)
	$Timer.start()
	

func _input(event):
	if event.is_action_pressed("pause"):
		get_tree().set_pause(!get_tree().paused)
		

func _on_Timer_timeout():
	if(restart): 
		OS.delay_msec(1000)
		$RestartScreen.visible = false
		restart = false
	
	$lblContract.text = str(data.get(str(turn)).get("truck").get("contract_list"))
	
	# Test if all upgrade textures fit and that I can change the sprite
	$UpgBody.texture = load(body_sprites[turn%3])
	$UpgTires.texture = load(tires_sprites[turn%4])
	$UpgAddOns.texture = load(addons_sprites[turn%3])
	
	# Show Events
	if(turn % 2 == 0):
		eventsDict["ice"]["active"] = true
	else: $EventIce.visible = false
		
	
	# TruckHUD moves up and down like a truck bouncing on the road. Keep or no?
	#if(turn % 2 == 0):
	#	$TruckHUD.position.y += 2
	#else:
	#	$TruckHUD.position.y -= 2
	
	turn += 1

var signSpeed = .06
var rockSpeed = .06
var iceSpeed = .06

var xdest = -1400
var ydest = 840

var xorig = 530
var yorig = 375

var originalPosition = Vector2(530,375)
var originalDistance = originalPosition.distance_to(Vector2(xdest,ydest))

var originalRPosition = Vector2(680,400)
var originalRDistance = originalRPosition.distance_to(Vector2(-xdest, ydest))

var originalIceDistance = Vector2(eventsDict.ice.originx,eventsDict.ice.originy).distance_to(Vector2(eventsDict.ice.destx,eventsDict.ice.desty))

func _process(delta):
	# Handling rock sprite
	if($Rock.position.y < 600):
		$Rock.position = $Rock.position.move_toward(Vector2(-xdest,ydest), delta * (rockSpeed + 20) )
		var currentRPosition = $Rock.position.distance_to(Vector2(-xdest,ydest))
		var newRScale = -25/originalRDistance * currentRPosition + 26
		$Rock.set_scale(Vector2(newRScale,newRScale))
		rockSpeed = rockSpeed * 1.05
	else:
		$Rock.set_position(Vector2(680,400))
		$Rock.scale.x = 1
		$Rock.scale.y = 1
		rockSpeed = .06
		
	# Handling sign sprite
	if($CitySign.position.y < 830):
		var currentPosition = $CitySign.position.distance_to(Vector2(xdest,ydest))
		var newScale = -25/originalDistance * currentPosition + 26
		$CitySign.position = $CitySign.position.move_toward(Vector2(xdest,ydest), delta * (signSpeed + 50) )
		$CitySign.set_scale(Vector2(newScale,newScale))
		signSpeed = signSpeed * 1.05
	else:
		$CitySign.set_position(Vector2(530,375))
		$CitySign.scale.x = 1
		$CitySign.scale.y = 1
		signSpeed = .06
	
	# Events -------------------------
	# Ice event
	if(eventsDict["ice"]["active"] and $EventIce/Sprite.position.y < eventsDict["ice"]["desty"] - 1):
		$EventIce.visible = true
		
		var currentDistance = $EventIce/Sprite.position.distance_to(Vector2(eventsDict["ice"]["destx"],eventsDict["ice"]["desty"]))
		var newScale = (-.577 * currentDistance + originalIceDistance*tan(PI/6))/20 + 1
		$EventIce/Sprite.set_scale(Vector2(newScale, newScale))
		$EventIce/Sprite.position = $EventIce/Sprite.position.move_toward(Vector2(eventsDict["ice"]["destx"],eventsDict["ice"]["desty"]), delta * (iceSpeed +50))
		iceSpeed = iceSpeed * 1.05
	else:
		eventsDict["ice"]["active"] = false
		$EventIce.visible = false
		$EventIce/Sprite.set_position(Vector2(eventsDict["ice"]["originx"],eventsDict["ice"]["originy"]))
		iceSpeed = .06
		
	
	
