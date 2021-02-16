extends AnimatedSprite

func _on_Timer_timeout():
	print("Here!")
	self.queue_free()

