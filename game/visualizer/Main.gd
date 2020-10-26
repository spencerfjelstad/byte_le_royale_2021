extends Node2D

var turn = 1
var data = {}

# Called when the node enters the scene tree for the first time.
func _ready():
	var file = File.new()
	file.open("../../logs/game_map.json", file.READ)
	var text = file.get_as_text()
	var result_json = JSON.parse(text)
	file.close()
	
	if result_json.error == OK:
		data = result_json.result
		
	$Turncounter.set_wait_time(1)
	$Turncounter.start()

func _on_Timer_timeout():
	$Label.text = str(data.get(str(turn)))
	turn += 1
	$Turncounter.set_wait_time(1)
