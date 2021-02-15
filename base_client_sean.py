from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.turn = 0
        self.queue = []
        self.low = 1000
        self.high = 2000

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'Team Name'

    def getMPG(self, speed):
        return (-0.002649444*(speed**2))+(.2520296*speed)+.22752

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
        dist = self.chooseBestRoad(truck.map.current_node.roads)
        return True if (dist.length/self.getMPG(truck.speed))/(truck.body.max_gas*100) - (dist.length * 1.1) > 0 else False

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
                score = contractList[index]['contract'].money_reward / self.calculateLength(contractList[index]['map'])
            else:
                score = contractList[index]['contract'].renown_reward / self.calculateLength(contractList[index]['map']) 
            if score > prevBest:
                prevBest = score
                bestIndex = index
        #print(bestIndex)
        return bestIndex

    def chooseBestContract2(self, truck, contractList):
        bestIndex = -1
        for index in range(len(contractList)):
            if self.turn < self.low and contractList[index]['contract'].difficulty == ContractDifficulty.easy:
                bestIndex = index
            elif self.turn < self.high and contractList[index]['contract'].difficulty == ContractDifficulty.medium:
                bestIndex = index
            elif self.turn > self.high and contractList[index]['contract'].difficulty == ContractDifficulty.hard:
                bestIndex = index
        #print(contractList[bestIndex]['contract'].difficulty == ContractDifficulty.easy)
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
        self.turn += 1
        if(truck.active_contract is None and ActionType.select_contract not in self.queue):
            # Select contract
            ind = self.chooseBestContract2(truck, truck.contract_list)
            actions.set_action(ActionType.select_contract, ind)
            print("Selecting index " + str(ind))
        elif ActionType.set_speed not in self.queue and (truck.speed != 47 and self.turn < self.high) or (truck.speed != 67 and self.turn > self.high):
            actions.set_action(ActionType.set_speed, 47) if self.turn < self.high else actions.set_action(ActionType.set_speed, 67)
            print('speed')
        elif ActionType.buy_gas not in self.queue and (( truck.map.current_node.next_node is not None and truck.map.current_node.gas_price > truck.map.current_node.next_node.gas_price and self.canIMakeIt(truck)) or not self.canIMakeIt(truck)):
                # Buy gas
                #print("Gas")
                actions.set_action(ActionType.buy_gas)
        elif ActionType.repair != self.queue[0] and truck.health < 75:
            actions.set_action(ActionType.repair)
            #print("Heal")
        elif ActionType.upgrade not in self.queue and truck.money > 1000 and (truck.tires != TireType.tire_normal and self.turn < self.high) or (truck.tires != TireType.monster_truck and self.turn > self.high):
            actions.set_action(ObjectType.tires, TireType.tire_normal) if self.turn < self.high else actions.set_action(ObjectType.tires, TireType.monster_truck)
        elif  (truck.body.level < 3 and (10000 * 1.2 * (truck.body.level + 1)) < truck.money) and ActionType.upgrade not in self.queue:
            #print("upgrade")
            actions.set_action(ActionType.upgrade, self.handleUpgrades(truck, ObjectType.tank, ObjectType.GPS))
        else:
            # Move to next node
            #print("move")
            actions.set_action(ActionType.select_route, self.chooseBestRoad(truck.map.current_node.roads))
        if len(self.queue) > 1:
            self.queue.pop(-1)
        self.queue.insert(0, actions._chosen_action)
             
        pass





