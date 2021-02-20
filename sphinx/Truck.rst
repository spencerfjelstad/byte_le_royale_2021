================
The Truck Object
================

The truck object holds everything related to the game. It should be noted that contract_list holds three
contracts with varying dificulty, with index 0 being the easy contract and index 2 holding the hard contract.

Instance variables
##################

================  =========================== ===================
Name               Type                        Description
================  =========================== ===================
contract_list      :doc:`./Contract` []        A list of contracts you can pick from
active_contract    :doc:`./Contract` or None   The current contract you are working to complete
body               :doc:`./BodyObjects`        Your current body Object. Default is a BaseBodyObject 
addons             :doc:`./AddonObjects`       Your current addon object. Default is a BaseUpgradeObject
tires              int                         The TireEnum you are currently equiped with. Default is tire_normal. More at :doc:`./TireObjects`
speed              int                         The speed your truck is currently traveling at
health             float                       The health of your truck. 
money              int                         The amount of money you currently have. 
renown             int                         Your score. The game is won by having the most renown
================  =========================== ===================

Please note that the BaseBodyObject gives you the default max_gas attribute. You can't switch back to the base objects once you upgrade


Truck Upgrade Negations
########################

Some truck upgrade has the potential to negate some of the time and damage penalties from events. Listed below are all
Negations. For more on upgrades, you can visit :doc:`./BodyObjects` , :doc:`./AddonObjects` , or :doc:`./TireObjects`

============================ =============================
Upgrade                         Negates
============================ =============================
ObjectType.headlights         EventType.animal_in_road
ObjectType.sentryGun          EventType.rock_slide
ObjectType.GPS                EventType.traffic
ObjectType.policeScanner      EventType.bounty_hunter
TireType.tire_sticky          EventType.icy_road
TireType.monster_truck        EventType.bandits
ObjectType.rabbitFoot         EventType.animal_in_road, EventType.bandits,EventType.icy_road, EventType.bounty_hunter, EventType.rock_slide, EventType.traffic
============================ =============================

