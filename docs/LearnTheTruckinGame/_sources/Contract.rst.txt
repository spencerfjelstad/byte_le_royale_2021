===================
Contract
===================

Contracts come in easy, medium and hard versions, which impact their rewards, renown, length and completabiltiy. 
Easy contracts give less renown and reward, but are also shorter. The opposite is true with hard contracts. Contract also contains the map :doc:`./GameMap` you need to traverse to complete the contract. Illegal contracts have all of the properties of a regular contract, however they also introduce the risk of getting caught by police. If caught you will receive a money penalty and a time penalty, as well as lose the contract. To compensate for this additional risk, the money and renown you receive for completing an illegal contract will be much greater than a normal contract. An illegal contract's risk can be reduced by upgrading the police scanner.

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

Additional instance variables for the illegal contract object

================  =========================== ===================
Name               Type                        Description
================  =========================== ===================
level              int                         The contraband level enum, representing how 
penalties          dict                        Dictionary containing penalty for getting caught by police. Keys are 'time_penalty' and 'money_penalty'
================  =========================== ===================
