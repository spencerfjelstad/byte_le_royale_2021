extends Node2D


export (PackedScene) var Ice
export (PackedScene) var RockSlide
export (PackedScene) var Animal
export (PackedScene) var Traffic
export (PackedScene) var Bandits

export (PackedScene) var Sign

# Rock starting place = 680, 400
var turn = 1
var restart = false
var turns = []
var data = {}

var eventsDict = {
	"ice": {
		"active": true,
		"originx": 600,
		"originy": 425,
		"destx": 600,
		"desty": 800,
		"sprite": "res://assets/events/event_icy_road.png"
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
	
	
	
	# Handle labels
	var name = str(data.get(str(turn)).get("truck").get("active_contract").get("name")) + "\n"
	var money_reward = "Payment: " + str(data.get(str(turn)).get("truck").get("active_contract").get("money_reward")) + "\n"
	var renown_reward = "Renown: " + str(data.get(str(turn)).get("truck").get("active_contract").get("renown_reward")) + "\n"
	var difficulty = "Difficulty: " + str(data.get(str(turn)).get("truck").get("active_contract").get("difficulty")) + "\n"
	
	$lblContract.text = name + money_reward + renown_reward + difficulty
	
	$lblSpeed.text = str(data.get(str(turn)).get("truck").get("speed")) + " MPH"
	$lblFuel.text = str(stepify(data.get(str(turn)).get("truck").get("body").get("current_gas"), 0.01) * 100) + "%"
	$lblHealth.text = str(stepify(data.get(str(turn)).get("truck").get("health"), 0.01))
	$lblTime.text = "Turn: " + str(turn)
	$lblMoney.text = str(data.get(str(turn)).get("truck").get("money"))
	$lblRenown.text = str(data.get(str(turn)).get("truck").get("renown"))
	
	# Test if all upgrade textures fit and that I can change the sprite
	$UpgBody.texture = load(body_sprites[turn%3])
	$UpgTires.texture = load(tires_sprites[turn%4])
	$UpgAddOns.texture = load(addons_sprites[turn%3])
	
	# Show Events
	if(turn % 3 == 0): spawn_bandits()
	
	# Variable for city sign
	spawn_sign("Plankton")
	# TruckHUD moves up and down like a truck bouncing on the road. Keep or no?
	#if(turn % 2 == 0):
	#	$TruckHUD.position.y += 2
	#else:
	#	$TruckHUD.position.y -= 2
	
	turn += 1

var signSpeed = 1
var rockSpeed = 1

var xdest = -1400
var ydest = 840

var xorig = 530
var yorig = 375

var originalPosition = Vector2(530,375)
var originalDistance = originalPosition.distance_to(Vector2(xdest,ydest))

var originalRPosition = Vector2(680,400)
var originalRDistance = originalRPosition.distance_to(Vector2(-xdest, ydest))

func _process(delta):
	# Handling rock sprite
	if($Rock.position.y < 600):
		$Rock.position = $Rock.position.move_toward(Vector2(-xdest,ydest), delta * (rockSpeed + 20) )
		var currentRPosition = $Rock.position.distance_to(Vector2(-xdest,ydest))
		var newRScale = -25/originalRDistance * currentRPosition + 26
		$Rock.set_scale(Vector2(newRScale,newRScale))
		rockSpeed = rockSpeed * 1.06
	else:
		$Rock.set_position(Vector2(680,400))
		$Rock.scale.x = 1
		$Rock.scale.y = 1
		rockSpeed = 1
		
	# Handling sign sprite
	#if($CitySign.position.y < 830):
	#	var currentPosition = $CitySign.position.distance_to(Vector2(xdest,ydest))
	#	var newScale = -25/originalDistance * currentPosition + 26
	#	$CitySign.position = $CitySign.position.move_toward(Vector2(xdest,ydest), delta * (signSpeed + 50) )
	#	$CitySign.set_scale(Vector2(newScale,newScale))
	#	signSpeed = signSpeed * 1.06
	#else:
	#	$CitySign.set_position(Vector2(530,375))
	#	$CitySign.scale.x = 1
	#	$CitySign.scale.y = 1
	#	signSpeed = 1
	
		
	
# Events
func spawn_ice(posX = eventsDict["ice"]["originx"], posY = eventsDict["ice"]["originy"]):
	var ice_instance = Ice.instance()
	add_child(ice_instance)
	move_child(ice_instance, 2)
	ice_instance.set_position(Vector2(posX,posY))
	
func spawn_rock_slide():
	var rock_slide_instance = RockSlide.instance()
	add_child(rock_slide_instance)
	move_child(rock_slide_instance, 2)
	pass

func spawn_traffic():
	var traffic_instance = Traffic.instance()
	add_child(traffic_instance)
	move_child(traffic_instance, 1)
	pass

func spawn_bandits():
	var bandits_instance = Bandits.instance()
	add_child(bandits_instance)
	move_child(bandits_instance, 3)
	pass
	
func spawn_animal():
	var animal_instance = Animal.instance()
	add_child(animal_instance)
	move_child(animal_instance, 2)
	pass

func spawn_sign(name):
	var city_sign_instance = Sign.instance()
	add_child(city_sign_instance)
	move_child(city_sign_instance, 2)
	city_sign_instance.set_city_name(name)
	pass
