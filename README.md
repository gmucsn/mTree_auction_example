# mTree Clock Auction Tutorial

This tutorial will step you through the development of a clock auction. The basic idea of this auction is that a single item will come up for auction. An institution will then announce to all agents that the item is accepting bids with a minimum price. 

The agents will then make bids however they see fit. In this case, each agent will have a min and max bid that they would be willing to pay. Additionally, agents will also include a bid increment which will dictate how much they will be willing to escalate the bid in the event that someone else has submitted a higher bid.

Once a bid is received by the institution, the institution will move the current price to the highest bid. The institution will then alert all agents to the current price. 

After each new high bid is registered, the institution will also send a message to itself to determine whether the auction should end. The institution will decide when to terminate the auction when more than 5 seconds have passed since the last bid.

# Steps to build this tutorial

Prereqs. Step 0 - In this step you will simply need to create the corresponding directories for your code

1. Step 1 - In this step we will define our initial code files for an environment, an institution, and an agent

2. Step 2 - We will complete the code for the environment

3. Step 3 - We will now provide minimal code for our institution to start and deliver the first price to the agents

4. Step 4 - We will now code the bidding capability for agents

5. Step 5 - We will modify the institution to have a proper closing rule