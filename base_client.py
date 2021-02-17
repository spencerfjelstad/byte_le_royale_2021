from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'Team Name'

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions, world, truck, time):
        """
        This is where your AI will decide what to do.
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you will add effort allocations or decrees to.
        :param world:       Generic world information
        """
        
        if(truck.active_contract is None):
            # Select contract
            print("Select")
            actions.set_action(ActionType.select_contract, 0)
        elif(truck.body.current_gas < .20):
            # Buy gas
            print("Gas")
            actions.set_action(ActionType.buy_gas)
            
        elif truck.health < 40 and truck.money > 1000:
            print("Heal")
            actions.set_action(ActionType.repair)
        elif  truck.body.level < 3 and 100000 * 1.2 * (truck.body.level + 1) < truck.money:
            print("upgrade")
            actions.set_action(ActionType.upgrade, ObjectType.tank)
        elif(truck.map.current_node.city_name != 'end'):
            # Move to next node
            print("move")
            actions.set_action(ActionType.select_route, truck.map.current_node.roads[0])
        

        
        pass
