extends Node2D

var turn = 1
var turns = []
var data = {}

func _ready():
	var file = File.new()
	file.open("../../logs/turn_logs.json", file.READ)
	var text = file.get_as_text()
	var result_json = JSON.parse(text)
	file.close()
	
	if result_json.error == OK:
		data = result_json.result
	
	$Label.text = str(data.get("1").get("time"))
	
	$Timer.set_wait_time(1)
	$Timer.start()


func _on_Timer_timeout():
	$Timer.set_wait_time(1)
	$Label.text = str(data.get(str(turn)))
	turn += 1
