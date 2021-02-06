from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.prevAction = -1

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'Team Name'

    def calculateLength(self,map):
        currNode = map.head
        totLen = 0
        while(currNode != None):
            shortest = 10000
            for x in currNode.roads:
               shortest = min(shortest, x.length)
            totLen += shortest
            currNode = currNode.next_node
        return totLen

    def canIMakeIt(self, truck):
        dist = self.chooseBestRoad(truck.current_node.roads)
        return True if ((dist.length / 4.5) / (truck.body.max_gas * 100)) > 0 else False

    def handleUpgrades(self, truck, bodyEnum, addonEnum):
        if truck.body.level < truck.addons.level:
            if truck.body.level < 3:
                return bodyEnum
        else:
            if truck.addons.level < 3:
                return addonEnum


    def chooseBestContract(self, truck, contractList):
        bestIndex = -1
        prevBest = -1
        score = 0
        for index in range(len(contractList)):
            if truck.money < 3000:
                score = contractList[index].money_reward / self.calculateLength(contractList[index].game_map)
            else:
                score = contractList[index].renown_reward / self.calculateLength(contractList[index].game_map) 
            if score > prevBest:
                prevBest = score
                bestIndex = index
        print(bestIndex)
        return bestIndex

    def chooseBestRoad(self,roads):
        shortest = 10000
        index = -1
        for x in range(len(roads)):
               if(shortest > roads[x].length):
                   index = roads[x]
        #print("move index: " + str(index))
        return index

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions, world, truck, time):
        """
        This is where your AI will decide what to do.
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you will add effort allocations or decrees to.
        :param world:       Generic world information
        """
        
        if(truck.active_contract is None and ActionType.select_contract != self.prevAction):
            # Select contract
            ind = self.chooseBestContract(truck, truck.contract_list)
            actions.set_action(ActionType.select_contract, ind)
            self.prevAction = ActionType.select_contract
            #print("Selecting index " + str(ind))
        elif truck.speed != 70 and self.prevAction != ActionType.choose_speed:
            actions.set_action(ActionType.choose_speed, 70)
            self.prevAction = ActionType.choose_speed
        elif truck.tires != TireType.tire_econ:
            actions.set_action(ObjectType.tires, TireType.tire_econ)
            self.prevAction = ActionType.choose_speed
        elif(truck.body.current_gas < .23 and ActionType.buy_gas != self.prevAction):
            # Buy gas
            if(truck.current_node.gas_price < truck.current_node.next_node.gas_price or self.canIMakeIt(truck)):
                #print("Gas")
                actions.set_action(ActionType.buy_gas)
                self.prevAction = ActionType.buy_gas
        elif truck.health < 50 and ActionType.repair != self.prevAction and ActionType.buy_gas != self.prevAction:
            #print("Heal")
            actions.set_action(ActionType.repair)
            self.prevAction = ActionType.repair
        elif  (truck.body.level < 3 and 100000 * 1.2 * (truck.body.level + 1) < truck.money) and ActionType.select_contract != self.prevAction:
            #print("upgrade")
            actions.set_action(ActionType.upgrade, self.handleUpgrades(truck, ObjectType.tank, ObjectType.policeScanner))
            self.prevAction = ActionType.upgrade
        elif(truck.current_node.city_name != 'end'):
            # Move to next node
            actions.set_action(ActionType.select_route, self.chooseBestRoad(truck.current_node.roads))
            self.prevAction = ActionType.select_route
             
        pass





