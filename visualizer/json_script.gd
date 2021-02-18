extends Node2D


export (PackedScene) var Ice
export (PackedScene) var RockSlide
export (PackedScene) var Animal
export (PackedScene) var Traffic
export (PackedScene) var Bandits
export (PackedScene) var Police

export (PackedScene) var Rock
export (PackedScene) var Sign

var universal_speed = 1

# Rock starting place = 680, 400
var turn = 1
var restart = false
var turns = []
var data = {}

var speed = ""
var fuel = ""
var renown = ""
var health = ""
var time = ""
var money = ""
var upg_addons = ""
var upg_addons_lvl = ""
var upg_body = ""
var upg_body_lvl = ""
var upg_tires = ""

var road_dict = {
	"1": "visualizer/assets/road_type/mountain_road.png",
	"2": "visualizer/assets/road_type/forest_road.png",
	"3": "visualizer/assets/road_type/tundra_road.png",
	"4": "visualizer/assets/road_type/highway_road.png",
	"5": "visualizer/assets/road_type/city_road.png",
	"6": "visualizer/assets/road_type/highway_road.png"
}

var eventsDict = {
	"ice": {
		"active": true,
		"originx": 600,
		"originy": 425,
		"destx": 600,
		"desty": 800,
		"sprite": "visualizer/assets/events/event_icy_road.png"
		},
	"rock": false
}

func _ready():
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
	elif event.is_action_pressed("faster"):
		if($Timer.wait_time > .135):
			$Timer.set_wait_time($Timer.wait_time / 2)
			universal_speed *= 2
		changed_game_speed()
	elif event.is_action_pressed("slower"):
		if($Timer.wait_time < 1):
			$Timer.set_wait_time($Timer.wait_time * 2)
			universal_speed /= 2
		changed_game_speed()
		

func _on_Timer_timeout():
	var file = File.new()
	var file_path = "./logs/turn_" + ("%04d" % turn) + ".json"
	if(!file.file_exists(file_path)):
		$GameOver.visible = true
		$GameOver.game_over = true
		
		# Set game over screen variables
		$GameOver/lblFinalRenown.text = "Renown: " + renown
		$GameOver/lblFinalFuel.text = "Fuel: " + fuel
		$GameOver/lblFinalSpeed.text = "Speed: " + speed
		$GameOver/lblFinalHealth.text = "Health: " + health
		$GameOver/lblFinalTime.text = "Time: " + time
		$GameOver/lblFinalMoney.text = "Money: " + money
		
		$GameOver/lblFinalAddOns.text = "Add Ons: " + upgrades_to_string(upg_addons) + " LVL " + str(upg_addons_lvl)
		$GameOver/lblFinalBody.text = "Body: " + upgrades_to_string(upg_body) + " LVL " + str(upg_body_lvl)
		$GameOver/lblFinalTires.text = "Tires: " + tires_to_string(upg_tires)
		
	else:
		file.open(file_path, file.READ)
		var text = file.get_as_text()
		var result_json = JSON.parse(text)
		file.close()
	
		if result_json.error == OK:
			data = result_json.result
	
	if(restart): 
		OS.delay_msec(2000)
		$RestartScreen.visible = false
		restart = false
	
	
	
	
	# Contracts
	var active_contract = data.get("truck").get("active_contract")
	var cname = ""
	var money_reward = ""
	var renown_reward = ""
	var difficulty = ""
	var next_city = ""
	if(active_contract != null):
		cname = active_contract.get("name") + "\n"
		money_reward = "Payment: " + str(data.get("truck").get("active_contract").get("money_reward")) + "\n"
		renown_reward = "Renown: " + str(data.get("truck").get("active_contract").get("renown_reward")) + "\n"
		difficulty = "Difficulty: " + str(data.get("truck").get("active_contract").get("difficulty")) + "\n"
		var next_city_value = data.get("truck").get("map").get("current_node").get("next_node")
		if(next_city_value != null):
			next_city = "Next city: " + next_city_value.get("city_name")
		else:
			next_city = "Next city: Not in route"
		
	else:
		cname = "No contract selected"
	
	$lblContract.text = cname + money_reward + renown_reward + difficulty + next_city
	
	# Handle labels
	# Save values for Game Over screen
	speed = str(data.get("truck").get("speed")) + " MPH"
	$lblSpeed.text = speed
	fuel =  str(stepify(data.get("truck").get("body").get("current_gas"), 0.01) * 100) + "%"
	$lblFuel.text = fuel
	health = str(stepify(data.get("truck").get("health"), 0.01))
	$lblHealth.text = health
	time = str(stepify(data.get("time"), 0.01))
	$lblTime.text = time
	money = str(data.get("truck").get("money"))
	$lblMoney.text = money
	renown = str(data.get("truck").get("renown"))
	$lblRenown.text = renown
	
	$lblTurn.text = "Turn: " + str(turn)
	
	var road_type = data.get("selected_route")
	change_road(road_type)
	
	var event_type = data.get("event")
	show_event(event_type)
	
	# If we're "moving", spawn moving things
	if(road_type != 0):
		spawn_rock()
		spawn_sign(str(data.get("truck").get("map").get("current_node").get("city_name")))
	
	# Save variables for Game Over screen
	upg_body = data.get("truck").get("body").get("object_type")
	show_upgrades_body(upg_body)
	upg_addons = data.get("truck").get("addons").get("object_type")
	show_upgrades_addons(upg_addons)
	upg_tires = data.get("truck").get("tires")
	show_upgrades_tires(upg_tires)
	
	upg_body_lvl = str(data.get("truck").get("body").get("level"))
	$lblBody.text = "Body\nLvl " + upg_body_lvl
	upg_addons_lvl = str(data.get("truck").get("addons").get("level"))
	$lblAddOns.text =  "Add Ons\nLvl " + upg_addons_lvl
	
	turn += 1

# Events
func spawn_ice(posX = eventsDict["ice"]["originx"], posY = eventsDict["ice"]["originy"]):
	var ice_instance = Ice.instance()
	add_child(ice_instance)
	move_child(ice_instance, 2)
	ice_instance.set_position(Vector2(posX,posY))
	ice_instance.set_universal_speed(universal_speed)
	
func spawn_rock_slide():
	var rock_slide_instance = RockSlide.instance()
	add_child(rock_slide_instance)
	move_child(rock_slide_instance, 2)
	rock_slide_instance.set_universal_speed(universal_speed)

func spawn_traffic():
	var traffic_instance = Traffic.instance()
	add_child(traffic_instance)
	move_child(traffic_instance, 2)
	traffic_instance.set_universal_speed(universal_speed)

func spawn_bandits():
	var bandits_instance = Bandits.instance()
	add_child(bandits_instance)
	move_child(bandits_instance, 3)
	bandits_instance.set_universal_speed(universal_speed)
	
func spawn_animal():
	var animal_instance = Animal.instance()
	add_child(animal_instance)
	move_child(animal_instance, 2)
	animal_instance.set_universal_speed(universal_speed)

func spawn_police():
	var police_instance = Police.instance()
	add_child(police_instance)
	move_child(police_instance, 10)
	police_instance.set_timer_wait_time($Timer.wait_time)

# Fauna
func spawn_sign(name):
	var city_sign_instance = Sign.instance()
	add_child(city_sign_instance)
	move_child(city_sign_instance, 2)
	city_sign_instance.set_city_name(name)
	city_sign_instance.set_universal_speed(universal_speed)
	
func spawn_rock():
	var rock_instance = Rock.instance()
	add_child(rock_instance)
	move_child(rock_instance, 2)
	rock_instance.set_universal_speed(universal_speed)
	
func change_road(road_type):
	if(road_type != 0):
		$Environment.texture = load(road_dict[str(road_type)])
		if(road_type == 6):
			$Road.play("interstate")
		else: 
			$Road.play("default")
		
func show_event(event_type):
	if(event_type != 0):
		if(event_type == 1):
			spawn_rock_slide()
		elif(event_type == 2):
			spawn_ice()
		elif(event_type == 3):
			spawn_animal()
		elif(event_type == 4):
			spawn_bandits()
		elif(event_type == 5):
			spawn_police()
		elif(event_type == 6):
			spawn_traffic()

func show_upgrades_body(upgrade_type):
	var texture = ""
	# None
	if(upgrade_type == 0):
		texture = "visualizer/assets/Upgrades/upgrades_none.png"
	# Tank	
	elif(upgrade_type == 9):
		texture = "visualizer/assets/upgrades/upgrades_body_tank.png"
	# Headlights
	elif(upgrade_type == 11):
		texture = "visualizer/assets/upgrades/upgrades_body_headlights.png"
	# Sentry Gun
	elif(upgrade_type == 12):
		texture = "visualizer/assets/upgrades/upgrades_body_sentry.png"
		
	$UpgBody.texture = load(texture)	
	
func show_upgrades_addons(upgrade_type):
	var texture = ""
	# None
	if(upgrade_type == 0):
		texture = "visualizer/assets/Upgrades/upgrades_none.png"
	# Police Scanner	
	elif(upgrade_type == 8):
		texture = "visualizer/assets/upgrades/upgrades_addons_policescanner.png"
	# Rabbit Foot
	elif(upgrade_type == 13):
		texture = "visualizer/assets/upgrades/upgrades_addons_rabbit_foot.png"
	# GPS
	elif(upgrade_type == 14):
		texture = "visualizer/assets/upgrades/upgrades_addons_GPS.png"
		
	$UpgAddOns.texture = load(texture)	

func show_upgrades_tires(upgrade_type):
	var texture = ""
	# Normal
	if(upgrade_type == 0):
		texture = "visualizer/assets/upgrades/upgrades_tires_normal.png"
	# Economy	
	elif(upgrade_type == 1):
		texture = "visualizer/assets/upgrades/upgrades_tires_economy.png"
	# Sticky
	elif(upgrade_type == 2):
		texture = "visualizer/assets/upgrades/upgrades_tires_sticky.png"
	# Monster Truck
	elif(upgrade_type == 3):
		texture = "visualizer/assets/upgrades/upgrades_tires_monster.png"
	
	$UpgTires.texture = load(texture)	
	
func upgrades_to_string(upgrade_type):
	# none
	if(upgrade_type == 0):
		return "None"
	# policeScanner = 8
	elif(upgrade_type == 8):
		return "Police Scanner"
	# tank = 9
	elif(upgrade_type == 9):
		return "Tank"
	# headlights = 11
	elif(upgrade_type == 11):
		return "Headlights"
	# sentryGun = 12
	elif(upgrade_type == 12):
		return "Sentry Gun"
	# rabbitFoot = 13
	elif(upgrade_type == 13):
		return "Rabbit Foot"
	# GPS = 14
	elif(upgrade_type == 13):
		return "GPS"
	else:
		return "ERROR: No upgrade type found"
		
func tires_to_string(upgrade_type):
	# tire_normal = 0
	if(upgrade_type == 0):
		return "Normal"
	# tire_econ = 1
	elif(upgrade_type == 1):
		return "Economy"
	# tire_sticky = 2
	elif(upgrade_type == 2):
		return "Sticky"
	# monster_truck = 3
	elif(upgrade_type == 3):
		return "Monster Truck"

func changed_game_speed():
	$lblGameSpeed.visible = true
	$lblGameSpeed.text = (str(1/$Timer.wait_time) + "X")
	$lblGameSpeed.modulate.a = 1
