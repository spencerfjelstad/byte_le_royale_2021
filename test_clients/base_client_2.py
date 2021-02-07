from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.costs_and_effectiveness = {
            ObjectType.policeScanner: {
                ScannerLevel.level_zero: 0,
                ScannerLevel.level_one: 300,
                ScannerLevel.level_two: 900,
                ScannerLevel.level_three: 2000

            },

            ObjectType.tank: {
                TankLevel.level_zero: 10,
                TankLevel.level_one: 300,
                TankLevel.level_two: 900,
                TankLevel.level_three: 2000

            },

            ObjectType.headlights: {
                HeadlightLevel.level_zero: 10,
                HeadlightLevel.level_one: 50,
                HeadlightLevel.level_two: 100,
                HeadlightLevel.level_three: 300
            },

            ObjectType.sentryGun: {
                SentryGunLevel.level_zero: 10,
                SentryGunLevel.level_one: 50,
                SentryGunLevel.level_two: 100,
                SentryGunLevel.level_three: 300
            },

            ObjectType.rabbitFoot: {
                RabbitFootLevel.level_zero: 10,
                RabbitFootLevel.level_one: 20,
                RabbitFootLevel.level_two: 40,
                RabbitFootLevel.level_three: 80
            },

            ObjectType.GPS: {
                GPSLevel.level_zero: 100,
                GPSLevel.level_one: 200,
                GPSLevel.level_two: 700,
                GPSLevel.level_three: 1400
            }
        }

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
            print("Select Contract")
            actions.set_action(ActionType.select_contract, 0)
        elif(truck.body.current_gas < .2 and truck.money > 300):
            # Buy gas
            print("Buy Gas")
            actions.set_action(ActionType.buy_gas)
        elif truck.health < 30 and truck.money > 1000:
            print("Heal")
            actions.set_action(ActionType.heal)
        elif  truck.body.level < 3 and self.costs_and_effectiveness[ObjectType.tank][truck.body.level +1] * 1.2 < truck.money:
            actions.set_action(ActionType.upgrade, ObjectType.tank)
            print(("Upgrade current level {} money {}, predicted ammount: {}".format(truck.body.level,truck.money,self.costs_and_effectiveness[ObjectType.tank][truck.body.level] * 1.1)))
        elif(truck.map.current_node.city_name is not 'end'):
            # Move to next node
            print("Move")
            actions.set_action(ActionType.select_route,
                               truck.map.current_node.roads[0])

        pass
