=============
Events
=============

Potential Events
###################

There are 6 EventTypes, animal_in_road, bandits, icy_road, police, rock_slide, traffic. Each event will do damage to your truck
and take time to resolve. The likelihood of an event happening is increased as your speed increases. EventType type enumerations can be 
accessed by EventType.event_type. For example, EventType.bandits

**Damage Penalty**

Below are the EventTypes and their base damage. Damage penalties will reduce your truck's health. This is calculated by the event's base damage multiplied by the contract difficulty + 1. For example, if you had an easy difficulty contract and you got pulled over by the police, you would take 11.65 * 1 damage. Damage can be reduced by upgrades or can be increased by contract difficulty. 


=============== ==============
Event Type       Base Damage
=============== ==============
animal_in_road    34.28
bandits           48
icy_road          30
police            11.65
rock_slide        31.16
traffic           20.51
=============== ==============

**Time Penalty**

Below are the EventTypes and their base time penalty. A time penalty will subtract time from your remaining time. This is calculated by the event's base time multiplied by the contract difficulty + 1. For example, if you had an easy difficulty contract and you got pulled over by the police, it would reduce your remaining time by 10.3 * 1. Time penalties can be reduced by upgrades or can be increased by contract difficulty. 

=============== ==============
Event Type       Base Time
=============== ==============
animal_in_road    3.5
bandits           2.5
icy_road          4
police            10.3
rock_slide        3.85
traffic           5.85
=============== ==============


