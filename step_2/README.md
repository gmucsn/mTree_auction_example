# mTree Clock Auction Tutorial - Step 2

In this step, we will be setting up our environment's code. 

We will then be adding code to clock_environment.py in our mes folder.

In particular, we will need to add a directive handler to respond to messages of "start_environment." 

Directives identify the code that will handle the receiving and processing of messages from other components in the MES. You will use a decorator like `@directive_decorator("start_environment")` immediately above your class method to indicate what directive the method will handle.

Minimally, for our environment we will need to respond to the "start_environment" directive. So we will add this code to our class:
```
@directive_decorator("start_environment")
def start_environment(self, message:Message):
    self.provide_endowment()
    self.start_auction()
```

Now we will need to provide code for both providing the endowment to our agents and also to start the auction.

The provide_endowment method will contact all agents and provide them with an initial endowment. We will set the endowment to 30 (or whatever number you'd like... you can even randomly generate the endowments if you'd prefer). We will be iterating over the class property agent_addresses which is provide by mTree and contains the addresses of all agent addresses.

```
def provide_endowment(self):
    endowment = 30
    for agent in self.agent_addresses:
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("set_endowment")  # Set the directive (refer to 3. Make Messages) - has to match reciever decorator
        new_message.set_payload({"endowment": endowment})
        self.send(agent, new_message )  # receiver_of_message, message
```

In this method, notice the use of the Message object. These Message objects are how communications are handled in mTree. You will create a new message and minimally set the directive for the message. You can also include a payload in the message which the recipient can examine. 

When you've constructed your message you will then be able to use the send method. `self.send(recipient, message_object)` will send a message to the recipient you provide an address for.

Finally, we'll send a start auction message to the institution in your MES. 
```
def start_auction(self):
    new_message = Message()  # declare message
    new_message.set_sender(self.myAddress)  # set the sender of message to this actor
    new_message.set_directive("start_auction")
    new_message.set_payload({"agents": self.agent_addresses})
    self.send(self.institutions[0], new_message)  # receiver_of_message, message
```
In this case, we will use `self.insitutions[0]` to get the address of the institution as we will only be using one institution here. In this case we will be forwarding the addresses of all agents to the institution as well.