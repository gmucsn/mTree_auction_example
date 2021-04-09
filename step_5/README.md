# mTree Clock Auction Tutorial - Step 5

In this step we will update the institution code to add an auction closing rule. We will also be adding some additional log statements. 

To close the auction we will use a rule that says that if no new bid comes in within 5 seconds of the last bid, close the auction. To do this we will actually need to have the institution send itself a wakeup message. This wakeup message will be specified to be delivered in 5 seconds. The wakeup message we will send to help us verify if the auction should be closed, we will be modifying the alert_agents_of_price method.

```
def alert_agents_of_price(self, current_price):
    for agent in self.agents:
            new_message = Message()  # declare message
            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
            new_message.set_directive("current_price")
            new_message.set_payload({"current_price": current_price})
            self.send(agent, new_message)  # receiver_of_message, message
    
    unixtime2 = time.time()
    self.last_bid_time = unixtime2
    wakeup_message = Message()  # declare message
    wakeup_message.set_sender(self.myAddress)  # set the sender of message to this actor
    wakeup_message.set_directive("check_auction_close")
    wakeup_message.set_payload({"bid_action_time": unixtime2})
    self.wakeupAfter( datetime.timedelta(seconds=5), payload=wakeup_message)
```

What you'll notice in this code is that after we alert the agents of the new prices, we will then determine the current time and create a new message we will deliver to the institution's check_auction_close directive.

We will then need to add a directive handler for check_auction_close. In this case we will implement the function to pull the bid_action_time contained in the message. This is the time at which this reminder was sent. We will then compare the time of the last bid to see if it occurred after the last recorded bid.

Also, what you will notice is that we have added a log_message method call. This is one way to record log messages in your experiment.

```
@directive_decorator("check_auction_close")
def check_auction_close(self, message:Message):
    bid_alert_time = message.get_payload()["bid_action_time"]
    if bid_alert_time < self.last_bid_time:
        self.log_message("Checking on auction... new bids received")
    elif (bid_alert_time - datetime.timedelta(seconds=5)) > (self.last_bid_time):
        self.log_message("Checking on auction... Auction should end")
        self.log_data("Final Price is: " + str(self.last_bid))
```

Also, we will go ahead and add a method call log_data in the bid_for_item directive handler. 

```
@directive_decorator("bid_for_item", message_schema=["bid"])
def bid_for_item(self, message: Message):
    bidder = message.get_sender()
    bid = int(message.get_payload()["bid"])
    self.log_data("Bid received " + str(bid))

    if bid > self.last_bid:
        self.last_bid = bid
        self.last_bid_time = time.time()
        self.bids.append((bid, bidder))
        self.alert_agents_of_price(self.last_bid)
```

            
            
        
