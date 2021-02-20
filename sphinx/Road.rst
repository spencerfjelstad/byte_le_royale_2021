================
Road
================

Roads are paths that connect :doc:`./Node` s. 

Instance variables
##################

================  ================== ===================
Name               Type                Description
================  ================== ===================
road_name          String             The name of the road
road_type          RoadType.Enum      The type of the road. Affects event probabilties
length             decimal            The length of the road
================  ================== ===================

RoadType Modifiers
##################

There are 6 RoadTypes, mountain_road, forest_road, tundra_road, city_road, highway, and interstate. RoadType enumerations can be accessed by RoadType.road_type. For example, RoadType.highway

**Length**

Some roads are longer than others. These roads will take longer to travel, so keep that in mind when choosing which road to go down! This is not determined by road type. 

**Potential Events**

<<<<<<< HEAD
The potential events that can happen on a given road type are listed below, in order of how often they occur. More on events can be seen at :doc:`./Events` 
=======
The potential events that can happen on a given RoadType are listed below. Once an event occurs, each road type has an order of which event is most likely to occur. For example, on the tundra road, an icy road is more likely to occur than a rock slide. Keep in mind, some events are more dangerous than others! It might be best to avoid those events as much as possible. More on events can be seen at :doc:`./Events` 
>>>>>>> 7b7d723d3ce5042d2658335e2f1d90b02fc9c920

============= ==============
Road          Events
============= ==============
mountain_road  rock_slide, animal_in_road, icy_road, police
forest_road   animal_in_road, police, rock_slide, icy_road
tundra_road   icy_road, police, rock_slide
city_road     bandits, police, traffic
highway       police, traffic
interstate    traffic, police
============= ==============