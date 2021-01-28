=============
Taking Action
=============

A critical part of building your bot is taking actions. The actions you can take are listed below.
All actions are set by calling
``
actions.set_action(ActionType.enum, {option})
``

Selecting a contract
####################

A list of contracts will be generated every turn. These contracts can be viewed in truck.contract_list
Once you have chosen a contract, pass the select contract enum and the index of the contract which you
wish to select. 

EX:
.. code-block:: python

actions.set_action(ActionType.select_contract, 0)

Will set your contract to the contract at index 0