extends Label

var alpha = 1.0

func _process(delta):
	if(self.visible == true and modulate.a > 0):
		modulate.a -= 0.8 * delta
	else:
		self.visible = false
