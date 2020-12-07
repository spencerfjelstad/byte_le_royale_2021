from game.common.TrUpgrades.tank import Tank
from game.common.TrUpgrades.police_scanner import PoliceScanner
from game.common.TrUpgrades.headlights import HeadLights
from game.common.TrUpgrades.sentry_gun import SentryGun
from game.common.TrUpgrades.rabbit_foot import RabbitFoot
from game.common.TrUpgrades.gps import GPS
from game.common.truck import Truck
from game.utils.helpers import getNextLevel
from game.utils import helpers
from game.common.stats import GameStats
from game.common.player import Player
from game.controllers.controller import Controller
from game.config import *
from game.common.enums import *
from collections import deque
import math
import random


class ActionController(Controller):
    def __init__(self):
        super().__init__()

        self.contract_list = list()

    def handle_actions(self, player, obj=None):
        player_action = player.action

        # Call the appropriate method for this action
        if(player_action == ActionType.buy_gas):
            raise NotImplementedError(
                "ActionType buy_gas hasn't been implemented yet")

        elif(player_action == ActionType.select_contract):
            # Checks if contract_list is empty. If so, we have a problem
            if(len(self.contract_list) == 0):
                raise ValueError(
                    "Contract list cannot be empty")

            # Selects the contract given in the player.action.contract_index
            self.select_contract(player)

        elif(player_action == ActionType.select_route):
            # Moves the player to the node given in the action_parameter
            self.move(player, player_action.action_parameter)

        elif(player_action == ActionType.upgrade):
            self.upgrade_level(self, player, obj)

    # Action Methods ---------------------------------------------------------

    def move(self, player, road):
        self.current_location = player.truck.current_node
        time_taken = 0
        for route in self.current_location.connections:
            if route is road:
                player.truck.current_node = route.city_2
                time_taken = road.length / player.truck.get_current_speed()
        player.time -= time_taken

    # Retrieve by index and store in Player, then clear the list
    def select_contract(self, player):
        player.active_contract = self.contract_list[int(
            player.action.contract_index)]
        self.contract_list.clear()

    def buy_gas(self, player):
        gasPrice = round(random.uniform(1, 5), 2)  # gas price per percent
        if(player.truck.current_node.node_type is NodeType.city and player.truck.money > 0):
            percentRemain = player.truck.max_gas - round(player.truck.gas, 2)
            maxPercent = round((player.truck.money / gasPrice) / 100, 2)
            if(percentRemain < maxPercent):
                player.truck.money -= percentRemain * gasPrice
                player.truck.gas = player.truck.max_gas
            else:
                player.truck.money = 0
                player.truck.money += maxPercent

    def upgrade_body(self, player, objEnum, typ):
        if objEnum is ObjectType.tank:
            # If the player doesn't currently have a tank and they have enough money for the base tank, give them a tank!
            if (not isinstance(player.truck.body, Tank)) and GameStats.gas_upgrade_cost[0] <= player.money:
                player.truck.body = Tank()
                player.money -= GameStats.gas_upgrade_cost[0]
            else:
                # otherwise, upgrade their current tank
                tnk = player.truck.body
                nxtLev = tnk.level + 1
                if tnk.level is not TankLevel.level_three and GameStats.gas_upgrade_cost[nxtLev] <= player.money:
                    player.money -= GameStats.gas_upgrade_cost[nxtLev]
                    player.truck.body.level = nxtLev
                else:
                    self.print("Not enough money or at max level for gas tank")
        if objEnum is ObjectType.headlights:
            if (not isinstance(player.truck.body, HeadLights)) and GameStats.headlight_upgrade_cost[0] <= player.money:
                player.truck.body = HeadLights()
                player.money -= GameStats.headlight_upgrade_cost[0]
            else:
                # otherwise, upgrade their current headlights
                lgt = player.truck.body
                nxtLev = lgt.level + 1
                if lgt.level is not HeadlightLevel.level_three and GameStats.headlight_upgrade_cost[nxtLev] <= player.money:
                    player.money -= GameStats.headlight_upgrade_cost[nxtLev]
                    player.truck.body.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for headlights")
        if objEnum is ObjectType.sentryGun:
            if (not isinstance(player.truck.body, SentryGun)) and GameStats.sentry_upgrade_cost[0] <= player.money:
                player.truck.body = SentryGun()
                player.money -= GameStats.sentry_upgrade_cost[0]
            else:
                # otherwise, upgrade their current sentry gun
                gn = player.truck.body
                nxtLev = gn.level + 1
                if gn.level is not SentryGunLevel.level_three and GameStats.sentry_upgrade_cost[nxtLev] <= player.money:
                    player.money -= GameStats.sentry_upgrade_cost[nxtLev]
                    player.truck.body.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for sentry gun")

    def upgrade_addons(self, player, objEnum, typ):
        if objEnum is ObjectType.policeScanner:
            # If the player doesn't currently have a scanner and they have enough money for the base scanner, give them a scanner!
            if (not isinstance(player.truck.addons, PoliceScanner)) and GameStats.scanner_upgrade_cost[0] <= player.money:
                player.truck.addons = PoliceScanner()
                player.money -= GameStats.scanner_upgrade_cost[0]
            else:
                # otherwise, upgrade their current scanner
                scn = player.truck.addons
                nxtLev = scn.level + 1
                if scn.level is not ScannerLevel.level_three and GameStats.scanner_upgrade_cost[nxtLev] <= player.money:
                    player.money -= GameStats.scanner_upgrade_cost[nxtLev]
                    player.truck.addons.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for police scanner")
        if objEnum is ObjectType.rabbitFoot:
            # If the player doesn't currently have a scanner and they have enough money for the base scanner, give them a scanner!
            if (not isinstance(player.truck.addons, RabbitFoot)) and GameStats.rabbit_foot_upgrade_cost[0] <= player.money:
                player.truck.addons = RabbitFoot()
                player.money -= GameStats.rabbit_foot_upgrade_cost[0]
            else:
                # otherwise, upgrade their current scanner
                ft = player.truck.addons
                nxtLev = ft.level + 1
                if ft.level is not RabbitFootLevel.level_three and GameStats.rabbit_foot_upgrade_cost[nxtLev] <= player.money:
                    player.money -= GameStats.rabbit_foot_upgrade_cost[nxtLev]
                    player.truck.addons.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for rabbit foot")
        if objEnum is ObjectType.GPS:
            # If the player doesn't currently have a scanner and they have enough money for the base scanner, give them a scanner!
            if (not isinstance(player.truck.addons, GPS)) and GameStats.GPS_upgrade_cost[0] <= player.money:
                player.truck.addons = GPS()
                player.money -= GameStats.GPS_upgrade_cost[0]
            else:
                # otherwise, upgrade their current scanner
                gp = player.truck.addons
                nxtLev = gp.level + 1
                if gp.level is not GPSLevel.level_three and GameStats.GPS_upgrade_cost[nxtLev] <= player.money:
                    player.money -= GameStats.GPS_upgrade_cost[nxtLev]
                    player.truck.addons.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for GPS")

    def upgrade_tires(self, player, objEnum, typ):
        tireLev = player.truck.tires
        if typ in TireType.__dict__.values() and typ is not tireLev and GameStats.tire_switch_cost <= player.money:
            player.truck.tires = typ
            player.money -= GameStats.tire_switch_cost
        else:
            self.print(
                "Either type is not in the enumeration, tiretype is already set to the type requested, or not enough money")

    def upgrade_level(self, player, objEnum, typ=1):
        """
        Handles upgrading various object for the truck.
        """
        try:
            if not isinstance(player, Player):
                self.print("The player argument is not a Player object.")
                return

            # If the objects enum is an addon type, pass off to addon upgrade method
            elif objEnum in GameStats.addonObjects:
                self.upgrade_addons(player, objEnum, typ)

            # If the objects enum is a body type, pass off to body upgrade method
            elif objEnum in GameStats.body_objects:
                self.upgrade_body(player, objEnum, typ)

            # The upgrade logic for tires is much simpler, but I have decided to modularize it for the sake of consistancy
            elif objEnum is ObjectType.tires:
                self.upgrade_tires(player, objEnum, typ)

            else:
                self.print(
                    "The object argument is not a valid upgradable object.")
                return
        except Exception as e:
            self.print(e)

    # End of Action Methods --------------------------------------------------
