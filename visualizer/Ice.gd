extends Sprite

var universal_speed = 1

var originx = 600
var originy = 425
var destx = 600
var desty = 800

var iceSpeed = 1

# How far away is the point I want to travel to?
# I need to know this to increase the speed and scale, but I only want to calculate it at the beginning.
var originalIceDistance = Vector2(originx,originy).distance_to(Vector2(destx,desty))

# This is a method that does the thing you want it to do. physics_process is a very stable method that doesn't rely on fps for timing. 
# It does your thing very quickly.
func _physics_process(delta: float) -> void:
	if(self.position.y < desty - 1):
		var currentDistance = self.position.distance_to(Vector2(destx, desty))
		# This trigonometry took me hours to figure out... basic trigonometry.
		# It sets the scale by changing the length as if it were a growing triangle going off the side of the road.
		# You probably don't need to know this
		var newScale = (-.577 * currentDistance + originalIceDistance*tan(PI/6))/20 + 1
		self.set_scale(Vector2(newScale,newScale))
		self.position = self.position.move_toward(Vector2(destx,desty), delta * (iceSpeed + 50) * universal_speed)
		iceSpeed = iceSpeed * 1.06
	# Delete the instance when it passes past a certain point
	else:
		self.queue_free()
		
func set_universal_speed(speed):
	universal_speed = speed
