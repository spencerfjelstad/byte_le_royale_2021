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
        # print(truck.current_node.city_name)
        
        print(truck.active_contract.__str__())
        
        if(truck.active_contract == None):
            # Select contract
            #print("Selecting contract " + truck.contract_list[0].__str__())
            actions.set_action(ActionType.select_contract, 0)
        elif(truck.current_node.roads[0] != None):
            # Move to next node
            print("Move")
            actions.set_action(ActionType.select_route, truck.current_node.roads[0])

        
        



        # actions.set_action(ActionType.select_route, truck.current_node.roads[0])
        

        
        pass
