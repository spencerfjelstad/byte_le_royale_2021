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
var team_name = ""

var road_dict = {
	"1": "visualizer/assets/road_type/mountain_road.png",
	"2": "visualizer/assets/road_type/forest_road.png",
	"3": "visualizer/assets/road_type/tundra_road.png",
	"4": "visualizer/assets/road_type/highway_road.png",
	"5": "visualizer/assets/road_type/city_road.png",
	"6": "visualizer/assets/road_type/highway_road.png"
}

# This never got used. Was an idea on how to organize object speeds and placements, but I ended up just moving them all to external scripts
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

# This function is our init. It's the first thing that runs. 
func _ready():
	# Make sure the TruckHUD is centered. This mattered more when I was trying to implement full screen.
	var viewportWidth = get_viewport().size.x
	var viewportHeight = get_viewport().size.y

	var scale = viewportWidth / $TruckHUD.texture.get_size().x

	# Optional: Center the sprite, required only if the sprite's Offset>Centered checkbox is set
	$TruckHUD.set_position(Vector2(viewportWidth/2, viewportHeight/2))

	# Set same scale value horizontally/vertically to maintain aspect ratio
	# If however you don't want to maintain aspect ratio, simply set different
	# scale along x and y
	$TruckHUD.set_scale(Vector2(scale, scale))
	
	# I ran each turn on a timer. You can make a timer by creating the node as a child. Make sure to make a "connections" on your timer.
	# My timer node has a connection (click on the wifi signal symbol) that calls _on_Timer_timeout() when the timer times out. 
	# Or just google a tutorial
	$Timer.set_wait_time(1)
	$Timer.start()
	
# This listens for an input, event, and calls the correct methods on that event. 
func _input(event):
	# The pause menu is mostly handled in the MenuPopup script. This just pauses the game.
	if event.is_action_pressed("pause"):
		get_tree().set_pause(!get_tree().paused)
	elif event.is_action_pressed("faster"):
		# This makes it so you can't speed up to infinity. Mostly because it broke when you sped it up too much.
		if($Timer.wait_time > .135):
			# Change the timer wait time to speed it up
			$Timer.set_wait_time($Timer.wait_time / 2)
			universal_speed *= 2
		# This method handles the UI informing the player of the change in speed.
		changed_game_speed()
	elif event.is_action_pressed("slower"):
		# This makes it so you can't slow down to infinity, because that's boring.
		if($Timer.wait_time < 1):
			# Change the timer wait time to speed it up
			$Timer.set_wait_time($Timer.wait_time * 2)
			universal_speed /= 2
		# This method handles the UI informing the player of the change in speed.
		changed_game_speed()
		
# This method is called when the timer times out. It handles changing turn information... mostly
func _on_Timer_timeout():
	
	# This wonderful beaut handles the JSON file input. 
	var file = File.new()
	# This gets the file path based off of which turn it is. Since each turn is a separate file, we have to change the number
	# at the end of the file to match the turn
	var file_path = "./logs/turn_" + ("%04d" % turn) + ".json"
	# If there is no JSON file, we assume that means it's GAME OVER
	if(!file.file_exists(file_path)):
		# Game over is an invisible node that I plop over the game to give the illusion it doesn't exist anymore.
		# I make it visible and start game over's code in a separate script. 
		$GameOver.visible = true
		$GameOver.game_over()
		
		# Set game over screen variables
		
		# I saved all the previous turns variables so I could use them for the game over screen. 
		# There's definitely a better way to do this, but I did this like day of or day before
		$GameOver/lblFinalRenown.text = "Renown: " + renown
		$GameOver/lblFinalFuel.text = "Fuel: " + fuel
		$GameOver/lblFinalSpeed.text = "Speed: " + speed
		$GameOver/lblFinalHealth.text = "Health: " + health
		$GameOver/lblFinalTime.text = "Time: " + time
		$GameOver/lblFinalMoney.text = "Money: " + money
		
		$GameOver/lblFinalAddOns.text = "Add Ons: " + upgrades_to_string(upg_addons) + " LVL " + str(upg_addons_lvl)
		$GameOver/lblFinalBody.text = "Body: " + upgrades_to_string(upg_body) + " LVL " + str(upg_body_lvl)
		$GameOver/lblFinalTires.text = "Tires: " + tires_to_string(upg_tires)
		
		$GameOver/lblFinalTeamName.text = "Team Name: " + team_name
		
	# If the JSON file was found	
	else:
		# Random file magic 
		file.open(file_path, file.READ)
		var text = file.get_as_text()
		var result_json = JSON.parse(text)
		file.close()
	
		# Data is my string that contains the entire turn file
		if result_json.error == OK:
			data = result_json.result
	
	# If people want to restart their run, I block out the screen and give objects time to pass by
	# The restart flag is changed in the MenuPopup script
	# This is bad
	if(restart): 
		OS.delay_msec(2000)
		$RestartScreen.visible = false
		restart = false
	
	
	
	# Get the values from the JSON and place on the screen
	# Contracts
	var active_contract = data.get("truck").get("active_contract")
	var cname = ""
	var money_reward = ""
	var renown_reward = ""
	var difficulty = ""
	var next_city = ""
	# If we have a contract
	if(active_contract != null):
		cname = active_contract.get("name") + "\n"
		money_reward = "Payment: " + str(data.get("truck").get("active_contract").get("money_reward")) + "\n"
		renown_reward = "Renown: " + str(data.get("truck").get("active_contract").get("renown_reward")) + "\n"
		difficulty = "Difficulty: " + str(data.get("truck").get("active_contract").get("difficulty")) + "\n"
		var next_city_value = data.get("truck").get("active_contract").get("game_map").get("current_node").get("next_node")
		if(next_city_value != null):
			next_city = "Next city: " + next_city_value.get("city_name")
		else:
			next_city = "Next city: Not in route"
	# If we don't have a contract
	else:
		cname = "No contract selected"
	
	# Display the information from the contract
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
	team_name = str(data.get("Team Name"))
	$lblTeamName.text = team_name
	
	var road_type = data.get("selected_route")
	change_road(road_type)
	
	var event_type = data.get("event")
	show_event(event_type)
	
	# If we're "moving", spawn moving things
	if(road_type != 0):
		spawn_rock()
		var contract = data.get("truck").get("active_contract")
		if(contract != null):
			spawn_sign(str(contract.get("game_map").get("current_node").get("city_name")))
	
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

# I handle moving objects like you would a bullet. 
# Check out this tutorial. This is what I used. https://www.youtube.com/watch?v=ggt05fCiH7M
# Basically I have created scenes for each moving object. I spawn an instance of those objects so I can shoot them like bullets. 
# The instance disappears when it reaches a certain distance
# If you want to see the scripts in the scene, check out the Ice.gd script
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
	
	
# These methods help keep the code less crazy looking. They just do a lot of enum checking
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
	# Display what speed the game is at. 
	$lblGameSpeed.text = (str(1/$Timer.wait_time) + "X")
	# This makes it disappear all spooky like 
	$lblGameSpeed.modulate.a = 1
