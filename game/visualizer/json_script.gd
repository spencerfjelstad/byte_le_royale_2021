extends Node2D

var turn = 1
var turns = []
var data = {}

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
	
	


func _on_Timer_timeout():
	$lblContract.text = str(data.get(str(turn)).get("truck").get("contract_list"))
	
	# Test if all upgrade textures fit and that I can change the sprite
	$UpgBody.texture = load(body_sprites[turn%3])
	$UpgTires.texture = load(tires_sprites[turn%4])
	$UpgAddOns.texture = load(addons_sprites[turn%3])
	
	turn += 1

