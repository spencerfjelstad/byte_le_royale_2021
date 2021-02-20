===================
Contract
===================

Contracts come in easy, medium and hard versions, which impact their rewards, renown, length and completability. 
Easy contracts give less renown and reward, but are also shorter. The opposite is true with hard contracts. Please note that 
in contract list you are given a dictionary where ['map'] is the game_map :doc:`./GameMap` you need to traverse to complete the contract
and ['contract'] is the contract object.

EX:

.. code-block:: python

    contractList[index]['contract']

will access a contract object at an associated index

Instance variables
##################

Below are the listed instance variables for the contract object

================  =========================== ===================
Name               Type                        Description
================  =========================== ===================
name               string                      The name of the current node you are on
region             Region.Enum                 The type of region the contract will be in. Impacts events
money_reward       int                         The amount of money you will recieve from completing this contract
renown_reward      int                         The amount of renown you will recieve from completing this contract
deadline           int                         The time you must complete the contract by. Decrements Automatically
difficulty         int                         The difficulty enum, where 0 is easy and 2 is hard
================  =========================== ===================

