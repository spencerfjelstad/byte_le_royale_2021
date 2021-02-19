extends Sprite

var universal_speed = 1

var originx = 600
var originy = 425
var destx = 600
var desty = 800

var iceSpeed = 1

var originalIceDistance = Vector2(originx,originy).distance_to(Vector2(destx,desty))

func _ready():
	self.set_position(Vector2(originx,originy))

func _physics_process(delta: float) -> void:
	if(self.position.y < desty - 1):
		var currentDistance = self.position.distance_to(Vector2(destx, desty))
		var newScale = (-.577 * currentDistance + originalIceDistance*tan(PI/6))/20 + 1
		self.set_scale(Vector2(newScale,newScale))
		self.position = self.position.move_toward(Vector2(destx,desty), delta * (iceSpeed + 50) * universal_speed)
		iceSpeed = iceSpeed * 1.06
	else: 
		self.queue_free()

func set_universal_speed(speed):
	universal_speed = speed
