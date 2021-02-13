extends Sprite

var originx = 530
var originy = 375
var destx = -1400
var desty = 840

var iceSpeed = 1

var originalIceDistance = Vector2(originx,originy).distance_to(Vector2(destx,desty))


func _physics_process(delta: float) -> void:
	if(self.position.y < desty - 1):
		var currentDistance = self.position.distance_to(Vector2(destx, desty))
		var newScale = (-.2 * currentDistance + originalIceDistance*tan(.2))/20 + 1
		self.set_scale(Vector2(newScale,newScale))
		self.position = self.position.move_toward(Vector2(destx,desty), delta * (iceSpeed + 50))
		iceSpeed = iceSpeed * 1.06
	else:
		self.queue_free()

func set_city_name(name):
	$lblCityName.text = name
