extends AnimatedSprite

func _on_Timer_timeout():
	self.queue_free()

func set_timer_wait_time(wait_time):
	$Timer.set_wait_time(wait_time)
