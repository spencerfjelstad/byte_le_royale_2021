extends Popup

var already_paused
var selected_menu = 0


var game_over = false
	
func _ready():
	$Restart.color = Color.gray
	$FinalTimer.set_wait_time(10)
	
	
	
func change_menu_color():
	$Restart.color = Color.black
	$Quit.color = Color.black
	
	match selected_menu:
		0:
			$Restart.color = Color.gray
		1:
			$Quit.color = Color.gray

func _input(event):
	if(game_over):
		if Input.is_action_just_pressed("ui_down"):
			selected_menu = (selected_menu + 1) % 2;
			change_menu_color()
		elif Input.is_action_just_pressed("ui_up"):
			if selected_menu > 0:
				selected_menu = selected_menu - 1
			else:
				selected_menu = 1
			change_menu_color()
		elif Input.is_action_just_pressed("ui_select"):
			match selected_menu:
				0:
					# Restart game
					game_over = false
					get_parent().turn = 1
					get_parent().restart = true
					get_parent().get_node("RestartScreen").visible = true
					#get_tree().paused = false
					self.visible = false
				1:
					# Quit game
					get_tree().quit()
					
# This method is called in json_script when game over is detected. It starts the timer for the end screen to close automatically.
# It needs to close automatically so the scrimmmage server can run through the games without needing input.
# If you have more time than 2 weeks you could try figuring out how to use a command to get the running exe to terminate. 
# This also sets my game_over flag to true so that the game over code works. 
func game_over():
	if(!game_over):
		$FinalTimer.start()
	game_over = true

# Close the game
func _on_FinalTimer_timeout():
	get_tree().quit()
