============
Body Objects
============

Body objects occupy the body attribute in the truck object. You can only have one Body object at a time. Aditionally the body object also holds the 
current_gas attribute, which is how much gas remains in your tank, and the max_gas attribute, which defaults to 1.

The Tank Object
###############

The Tank object increases the max_gas attribute. The levels are below

=====  ================== =====
Level  Max_Gas_multiplier Cost
=====  ================== =====
0      1                   10
1      1.5                 300
2      2                   900
3      4                   2000
=====  ================== =====

The Sentry Gun Object
#####################

The sentry gun object deters thieves and intimidates cops. It will reduce your damage to 