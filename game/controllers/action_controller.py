from game.common.TrUpgrades.BodyObjects.tank import Tank
from game.common.TrUpgrades.police_scanner import PoliceScanner
from game.common.TrUpgrades.BodyObjects.headlights import HeadLights
from game.common.TrUpgrades.BodyObjects.sentry_gun import SentryGun
from game.common.TrUpgrades.rabbit_foot import RabbitFoot
from game.common.TrUpgrades.gps import GPS
from game.common.truck import Truck
from game.utils import helpers
from game.common.stats import GameStats
from game.common.player import Player
from game.controllers.controller import Controller
from game.controllers.event_controller import EventController
from game.config import *
from game.controllers import event_controller
from game.common.enums import *

from collections import deque
import math
import random


class ActionController(Controller):
    def __init__(self):
        super().__init__()
        self.event_controller = EventController()
        self.contract_list = list()

    def handle_actions(self, player):
        player_action = player.action._chosen_action
        # Without a contract truck has no node to move to, ensure a contract is always active
        if player.truck.active_contract is not None or player_action == ActionType.select_contract:
            # Call the appropriate method for this action
            if(player_action == ActionType.select_contract):
                # Checks if contract_list is empty. If so, we have a problem
                if(len(self.contract_list) == 0):
                    raise ValueError("Contract list cannot be empty")
                # Selects the contract given in the player.action.action_parameter
                self.select_contract(player)
                player.time -= 1
                return ActionType.select_contract
            elif(player_action == ActionType.select_route):
                # Moves the player to the node given in the action_parameter
                #self.move(player, player_action.action.action_parameter)
                self.move(player)
                return ActionType.select_route
        if(player_action == ActionType.buy_gas):
            self.buy_gas(player)
            player.time -= GameStats.gas_pumping_time_penalty
            return ActionType.buy_gas
        elif(player_action == ActionType.repair):
            self.heal(player)
            player.time -= GameStats.repair_pumping_time_penalty
            return ActionType.repair
        elif(player_action == ActionType.upgrade):
            self.upgrade_level(player, player.action.action_parameter)
            player.time -= GameStats.upgrade_time_penalty
            return ActionType.upgrade
        elif(player_action == ObjectType.tires):
            self.upgrade_tires(player, player.action.action_parameter)
            player.time -= GameStats.upgrade_time_penalty
            return ActionType.upgrade
        elif(player_action == ActionType.set_speed):
            #This is an ActionType because the user client cannot directly influence truck values. 
            player.truck.set_current_speed(player.action.action_parameter)
            player.time -= 1
            return ActionType.set_speed
        else:
            self.print("Action aborted: no active contract!")
            return ActionType.none

    # Action Methods ---------------------------------------------------------    
    def move(self, player):
        road = player.action.action_parameter
        self.current_location = player.truck.map.current_node
        time_taken = 0
        fuel_efficiency = GameStats.getMPG(player.truck.speed) * GameStats.costs_and_effectiveness[ObjectType.tires]['fuel_efficiency'][player.truck.tires]
        for route in self.current_location.roads:
            if route == road:  # May need to be redone
                player.truck.map.get_next_node()
                self.event_controller.event_chance(road, player, player.truck)
                time_taken = (road.length / player.truck.get_current_speed())
                gas_used = (road.length/fuel_efficiency)/(player.truck.body.max_gas*100)
                player.truck.body.current_gas -= gas_used
                player.time -= time_taken

    # Retrieve by index and store in Player, then clear the list
    def select_contract(self, player):
        if len(self.contract_list) > int(player.action.action_parameter) and int(player.action.action_parameter) >= -1:
            selection = self.contract_list[int(player.action.action_parameter)]
            player.truck.active_contract = selection['contract']
            player.truck.map = selection['map']
            self.contract_list.clear()
        else:
            raise Exception("Contract list index was out of bounds")

    def buy_gas(self, player):
        # Gas price is tied to node
        gasPrice = player.truck.map.current_node.gas_price
        if(player.truck.money > 0):
            # Calculate what percent empty is the gas tank
            percentGone = (1 - (round(player.truck.body.current_gas, 2) / player.truck.body.max_gas))
            # Calculate the percentage the player could potentially buy
            maxPercent = round((player.truck.money / gasPrice) / 100, 2)
            if(percentGone < maxPercent):
                # If they can afford to fill up all the way, fill em up
                player.truck.money -= (percentGone * 100) * gasPrice
                player.truck.body.current_gas = player.truck.body.max_gas
            else:
                # Otherwise, give them the max percentage they can buy
                player.truck.money = 0
                player.truck.body.current_gas += (
                    maxPercent * player.truck.body.max_gas)

    def heal(self, player):
        healPrice = player.truck.map.current_node.repair_price
        if(player.truck.money > 0):
            # Calculate what percent repair is missing
            percentRemain = 1 - (round(player.truck.health, 2) / GameStats.truck_starting_health)
            # Calculate what percent repair they can afford
            maxPercent = round((player.truck.money / healPrice) / 100, 2)
            if(percentRemain < maxPercent):
                # If they can afford it, repair the truck all the way
                player.truck.money -= (percentRemain * 100) * healPrice
                player.truck.health = GameStats.truck_starting_health
            else:
                # Otherwise, do the maximum repairs
                player.truck.money = 0
                player.truck.health += maxPercent

    def upgrade_body(self, player, objEnum, typ):
        if objEnum is ObjectType.tank:
            # If the player doesn't currently have a tank and they have enough money for the base tank, give them a tank!
            if (not isinstance(player.truck.body, Tank)) and GameStats.costs_and_effectiveness[ObjectType.tank]['cost'][0] <= player.truck.money:
                player.truck.body = Tank()
                player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.tank]['cost'][0]
            else:
                # otherwise, upgrade their current tank
                tnk = player.truck.body
                nxtLev = tnk.level + 1
                if tnk.level is not TankLevel.level_three and GameStats.costs_and_effectiveness[ObjectType.tank]['cost'][nxtLev] <= player.truck.money:
                    player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.tank]['cost'][nxtLev]
                    player.truck.body.level = nxtLev
                else:
                    self.print("Not enough money or at max level for gas tank")
        if objEnum is ObjectType.headlights:
            if (not isinstance(player.truck.body, HeadLights)) and GameStats.costs_and_effectiveness[ObjectType.headlights]['cost'][0] <= player.truck.money:
                player.truck.body = HeadLights()
                player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.headlights]['cost'][0]
            else:
                # otherwise, upgrade their current headlights
                lgt = player.truck.body
                nxtLev = lgt.level + 1
                if lgt.level is not HeadlightLevel.level_three and GameStats.costs_and_effectiveness[ObjectType.headlights]['cost'][nxtLev] <= player.truck.money:
                    player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.headlights]['cost'][nxtLev]
                    player.truck.body.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for headlights")
        if objEnum is ObjectType.sentryGun:
            if (not isinstance(player.truck.body, SentryGun)) and GameStats.costs_and_effectiveness[ObjectType.sentryGun]['cost'][0] <= player.truck.money:
                player.truck.body = SentryGun()
                player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.sentryGun]['cost'][0]
            else:
                # otherwise, upgrade their current sentry gun
                gn = player.truck.body
                nxtLev = gn.level + 1
                if gn.level is not SentryGunLevel.level_three and GameStats.costs_and_effectiveness[ObjectType.sentryGun]['cost'][nxtLev] <= player.truck.money:
                    player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.sentryGun]['cost'][nxtLev]
                    player.truck.body.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for sentry gun")

    def upgrade_addons(self, player, objEnum, typ):
        if objEnum is ObjectType.policeScanner:
            # If the player doesn't currently have a scanner and they have enough money for the base scanner, give them a scanner!
            if (not isinstance(player.truck.addons, PoliceScanner)) and GameStats.costs_and_effectiveness[ObjectType.policeScanner]['cost'][0] <= player.truck.money:
                player.truck.addons = PoliceScanner()
                player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.policeScanner]['cost'][0]
            else:
                # otherwise, upgrade their current scanner
                scn = player.truck.addons
                nxtLev = scn.level + 1
                if scn.level is not ScannerLevel.level_three and GameStats.costs_and_effectiveness[ObjectType.policeScanner]['cost'][nxtLev] <= player.truck.money:
                    player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.policeScanner]['cost'][nxtLev]
                    player.truck.addons.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for police scanner")
        if objEnum is ObjectType.rabbitFoot:
            # If the player doesn't currently have a scanner and they have enough money for the base rabbit foot, give them a foot!
            if (not isinstance(player.truck.addons, RabbitFoot)) and GameStats.costs_and_effectiveness[ObjectType.rabbitFoot]['cost'][0] <= player.truck.money:
                player.truck.addons = RabbitFoot()
                player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.rabbitFoot]['cost'][0]
            else:
                # otherwise, upgrade their current scanner
                ft = player.truck.addons
                nxtLev = ft.level + 1
                if ft.level is not RabbitFootLevel.level_three and GameStats.costs_and_effectiveness[ObjectType.rabbitFoot]['cost'][nxtLev] <= player.truck.money:
                    player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.rabbitFoot]['cost'][nxtLev]
                    player.truck.addons.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for rabbit foot")
        if objEnum is ObjectType.GPS:
            # If the player doesn't currently have a scanner and they have enough money for the base scanner, give them a scanner!
            if (not isinstance(player.truck.addons, GPS)) and GameStats.costs_and_effectiveness[ObjectType.GPS]['cost'][0] <= player.truck.money:
                player.truck.addons = GPS()
                player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.GPS]['cost'][0]
            else:
                # otherwise, upgrade their current scanner
                gp = player.truck.addons
                nxtLev = gp.level + 1
                if gp.level is not GPSLevel.level_three and GameStats.costs_and_effectiveness[ObjectType.GPS]['cost'][nxtLev] <= player.truck.money:
                    player.truck.money -= GameStats.costs_and_effectiveness[ObjectType.GPS]['cost'][nxtLev]
                    player.truck.addons.level = nxtLev
                else:
                    self.print(
                        "Not enough money or at max level for GPS")

    def upgrade_tires(self, player, typ):
        tireLev = player.truck.tires
        if typ in TireType.__dict__.values() and typ is not tireLev and GameStats.tire_switch_cost <= player.truck.money:
            player.truck.tires = typ
            player.truck.money -= GameStats.tire_switch_cost
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
                player.truck.addons.update()
            # If the objects enum is a body type, pass off to body upgrade method
            elif objEnum in GameStats.body_objects:
                self.upgrade_body(player, objEnum, typ)
                player.truck.body.update()
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
