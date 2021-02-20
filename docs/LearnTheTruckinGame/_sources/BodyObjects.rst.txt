============
Body Objects
============

Body objects occupy the body attribute in the truck object. You can only have one Body object at a time. Additionally the body object also holds the 
current_gas attribute, which is how much gas remains in your tank, and the max_gas attribute, which defaults to 1.

The Tank Object
###############

The Tank object increases the max_gas attribute. Gas levels are stored as percents, IE level 1 holds 50% more gas than level 0.
Not having the Tank object leaves your truck with a level 0 tank.
Referenced as:

.. code-block:: python

    ObjectType.tank

The levels are below

=====  ================== =====
Level  Max_Gas_multiplier Cost
=====  ================== =====
0      1                   5400
1      1.5                 10800
2      2                   16200
3      4                   21600
=====  ================== =====

The Sentry Gun Object
#####################

The sentry gun will shoot boulders out of the road as you pass. It reduces damage and time taken by the rockslide event.
Referenced as:

.. code-block:: python

    ObjectType.sentryGun

The levels are below

=====  ================== ======
Level    Negation          Cost
=====  ================== ======
0       0.1                5400
1       0.2                10800
2       0.35               16200
3       0.5                21600
=====  ================== ======

The Headlights Object
#####################

The headlights object will increases the brightness of your headlights allowing you to react to animals in the road quicker.
It reduces damage and time taken by the animal_in_road event.

.. code-block:: python

    ObjectType.headlights

The levels are below

=====  ================== ======
Level    Negation          Cost
=====  ================== ======
0       0.1                5400
1       0.2                10800
2       0.35               16200
3       0.5                21600
=====  ================== ======