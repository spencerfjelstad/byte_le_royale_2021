===================
Game Map
===================

The game map is a linked list of nodes. Traveling to the next node requires selecting a valid road from your current node.
There can be 2-3 roads to choose from, but they all end up at the same location.

Instance variables
##################

================  =========================== ===================
Name               Type                        Description
================  =========================== ===================
head               :doc:`./Node`                The node the contract starts at
current_node       :doc:`./Node`                The node you are currently at
================  =========================== ===================

