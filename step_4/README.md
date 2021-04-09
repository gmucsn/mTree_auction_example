# mTree Clock Auction Tutorial - Step 4

In this step, we will be setting up our agent code. We will also generate a configuration file that we can use to run our current code and test it.

Here we will implement two directive handlers: set_endowment and current_price. 

The set_endowment directive handles a message from the environment that specifies the endowment for the agent. All we need to do here is take the endowment specified by the environment and save it to the agent.

```
@directive_decorator("set_endowment")
def set_endowment(self, message: Message):
    self.endowment = message.get_payload()["endowment"]
```

Next, we will want to implement the directive for handling current_price directives coming from the institution. In our implementation the agent we will see the current price that the institution has recorded as the max bid. The agent will then decide to make a bid or not and send this bid to the institution.

```
@directive_decorator("current_price", message_schema=["value"], message_callback="make_bid")
def bid_at_price(self, message: Message):
    self.current_price = message.get_payload()["current_price"]
    self.institution = message.get_sender()
    if self.current_price < self.max_bid:
        self.make_bid()
```

If you notice, the last two lines of this code block makes the determination about whether to bid or not. If the agent decides to make a bid they will use the make_bid method we will add to the agent.

```
def make_bid(self):
    new_message = Message()  # declare message
    new_message.set_sender(self.myAddress)  # set the sender of message to this actor
    new_message.set_directive("bid_for_item")
    self.last_bid = self.current_price + self.bid_increment
    new_message.set_payload({"bid": self.last_bid})
    self.send(self.institution, new_message)  # receiver_of_message, message
```

In order to support these functions we will be updating our __init__ method to specify certain properties.  In particular, we will have a property for the agent's endowment and will also specify the max_bid and bid_increment we would like to use.

```
def __init__(self):
    self.endowment = None
    self.institution = None
    self.item_for_bidding = None

    self.last_bid = 0

    self.max_bid = random.randint(5, 150)
    self.bid_increment = random.randint(1, 10)
```

Now that we have code for every component of our MES, we can run our experiment. In order to run our experiment we will need to build a configuration file. This is a json file that contains information about the components we will be using in our experiment.

We will create a new file in the config directory. We will call this file base_simulation.json. The contents of this file will look like:

```
{"mtree_type": "mes_simulation_description",
   "name":"Basic Clock Auction Run",
   "id": "1",
   "environment": "clock_environment.ClockEnvironment",
   "institution": "clock_institution.ClockInstitution",
   "number_of_runs": 1,
   "agents": [{"agent_name": "clock_simple_agent.ClockSimpleAgent", "number": 5}],
   "properties": {}
 }
```

The key components of this configuration file are the environment, institution, and agents properties. For the environment we will specify the file and class name of our environment, in this case clock_environment.ClockEnvironment. We will do the same for our institution by specifying clock_institution.ClockInstitution. Finally, we will add our agent as a dictionary in the agents property. The agents property actually allows us to specify different types of agents and the number of the agents we would like to be in our MES. Here we will specify the agent_name as clock_simple_agent.ClockSimpleAgent and the number is 5.

In order then to run this we will run the following command in the command line in the root direction of this tutorial `mTree_developer_server`. This will launch the mTree appication and a browser. You will then want to select the step_4 MES. Then click the configurations button. Then click the basic_simulation configuraiton. Finally, click the "Run Configuration" button and this will run your MES. You will notice a logs directory gets created in the step_4 directory, but you'll notice the log messages could be improved.



            
            
        
