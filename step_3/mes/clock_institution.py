from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import math
import random
import logging
import time
import datetime


@directive_enabled_class
class ClockInstitution(Institution):
    def __init__(self):
        self.auctions = 10
        self.min_item_value = 10
        self.max_item_value = 100

        self.last_bid = 0
        self.last_bid_time = 0

        self.starting_price = None
        self.bids = []

    @directive_decorator("start_auction", message_schema=["agents"], message_callback="send_agents_start")
    def start_auction(self, message:Message):
        if self.auctions > 0:
            self.auctions -= 1
            self.agents = message.get_payload()["agents"]
            self.bids = []
            self.starting_price = random.randint(self.min_item_value, self.max_item_value)
            self.alert_agents_of_price(self.starting_price)

    def alert_agents_of_price(self, current_price):
        for agent in self.agents:
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("current_price")
                new_message.set_payload({"current_price": current_price})
                self.send(agent, new_message)  # receiver_of_message, message

    @directive_decorator("bid_for_item", message_schema=["bid"])
    def bid_for_item(self, message: Message):
        bidder = message.get_sender()
        bid = int(message.get_payload()["bid"])
        if bid > self.last_bid:
            self.last_bid = bid
            self.last_bid_time = time.time()
            self.bids.append((bid, bidder))
            self.alert_agents_of_price(self.last_bid)
            
            
        
