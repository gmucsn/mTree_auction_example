# mTree Clock Auction Tutorial - Step 3

In this step, we will be setting up our institution's code. 

We will then be adding code to clock_institution.py in our mes folder. In particular, we will need to implement several directive handlers. Here we will be implementing a directive handler for start_auction which is a message we will receive from the environment. We will then implement a directive handler for handling bids from agents.

Starting with the start_auction directive handler we will implement a method that will determine what price to start the auction at. We will then alert all the agents of the price by calling another method we will call alert_agents_of_price.

```
@directive_decorator("start_auction", message_schema=["agents"], message_callback="send_agents_start")
def start_auction(self, message:Message):
    if self.auctions > 0:
        self.auctions -= 1
        self.agents = message.get_payload()["agents"]
        self.bids = []
        self.starting_price = random.randint(self.min_item_value, self.max_item_value)
        self.alert_agents_of_price(self.starting_price)
```

We will use the alert_agents_of_price method because we can then reuse the method for alerting all agents of price changes.

```
def alert_agents_of_price(self, current_price):
    for agent in self.agents:
            new_message = Message()  # declare message
            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
            new_message.set_directive("current_price")
            new_message.set_payload({"current_price": current_price})
            self.send(agent, new_message)  # receiver_of_message, message
```

Finally, we will implement a directive handler for accepting bids from agents. This will handle the handle_bid directive. This method will identify the bid amount from the agent and then compare this bid to the current high price. If the bid is above the current high price, then the new bid becomes the high price and we will then alert all agents of the new price.

```
@directive_decorator("bid_for_item", message_schema=["bid"])
def bid_for_item(self, message: Message):
    bidder = message.get_sender()
    bid = int(message.get_payload()["bid"])
    
    if bid > self.last_bid:
        self.last_bid = bid
        self.last_bid_time = time.time()
        self.bids.append((bid, bidder))
        self.alert_agents_of_price(self.last_bid)
```

Also, we will specify some properties for our class in the __init__ method. 

```
def __init__(self):
    self.auctions = 10
    self.min_item_value = 10
    self.max_item_value = 100

    self.last_bid = 0
    self.last_bid_time = 0

    self.starting_price = None
    self.bids = []
```





            
            
        
