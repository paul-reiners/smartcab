# P4: Train a Smart Cab to Drive

## Implement a basic driving agent

We first produce some random move/action `(None, 'forward', 'left', 'right')`.
Then we run this agent within the simulation environment with `enforce_deadline` set to `False`.

*In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?*

The agent moves randomly.  If I waited long enough, it would probably eventually make it to the target location, but
I've never seen it do so.

## Identify and update state

*Justify why you picked these set of states, and how they model the agent and its environment.*

I picked the following states:

* left
* right
* oncoming
* light

These four states seem like a good start.  I might add later the agent's current location.

## Implement Q-Learning

Using 
[Artificial Intelligence - foundations of computational agents -- 11.3.3 Q-learning](http://artint.info/html/ArtInt_265.html) by David Poole and Alan Mackworth as a reference, I implemented Q-learning.  At this point, I also added
one more item to the agent's state:

* next_waypoint

My agent seemed a bit more purposeful at this point.  It did reach the goal several times (with `enforce_deadline` still set to `False`) as I watched it.

At this point, I decided to start recording the exact results.  I now had the following settings:

* state: left, right, oncoming, light, next_waypoint
* discount (gamma): 0.9
* step size (alpha): 0.2

Here is the abridged output running with those settings:

	Simulator.run(): Trial 0
	Environment.reset(): Trial set up with start = (8, 3), destination = (2, 6), deadline = 45
	Environment.reset(): Primary agent could not reach destination within deadline!

	Simulator.run(): Trial 1
	Environment.reset(): Trial set up with start = (5, 6), destination = (2, 3), deadline = 30
	Environment.act(): Primary agent has reached destination!
	LearningAgent.update(): deadline = 6, inputs = {'light': 'green', 'oncoming': None, 'right': None, 'left': None}, action = forward, reward = 12

	Simulator.run(): Trial 2
	Environment.reset(): Trial set up with start = (5, 5), destination = (2, 6), deadline = 20
	Environment.act(): Primary agent has reached destination!
	LearningAgent.update(): deadline = 7, inputs = {'light': 'green', 'oncoming': None, 'right': None, 'left': None}, action = forward, reward = 10.5

	Simulator.run(): Trial 3
	Environment.reset(): Trial set up with start = (7, 1), destination = (4, 4), deadline = 30
	Environment.reset(): Primary agent could not reach destination within deadline!

	Simulator.run(): Trial 4
	Environment.reset(): Trial set up with start = (3, 4), destination = (5, 2), deadline = 20
	Environment.reset(): Primary agent could not reach destination within deadline!

	Simulator.run(): Trial 5
	Environment.reset(): Trial set up with start = (7, 6), destination = (3, 4), deadline = 30
	Environment.reset(): Primary agent could not reach destination within deadline!

	Simulator.run(): Trial 6
	Environment.reset(): Trial set up with start = (4, 1), destination = (4, 6), deadline = 25
	Environment.act(): Primary agent has reached destination!
	LearningAgent.update(): deadline = 21, inputs = {'light': 'green', 'oncoming': None, 'right': None, 'left': None}, action = forward, reward = 12

	Simulator.run(): Trial 7
	Environment.reset(): Trial set up with start = (6, 3), destination = (4, 5), deadline = 20
	Environment.act(): Primary agent has reached destination!
	LearningAgent.update(): deadline = 3, inputs = {'light': 'red', 'oncoming': None, 'right': None, 'left': None}, action = right, reward = 12

	Simulator.run(): Trial 8
	Environment.reset(): Trial set up with start = (6, 2), destination = (8, 6), deadline = 30
	Environment.act(): Primary agent has reached destination!
	LearningAgent.update(): deadline = 13, inputs = {'light': 'red', 'oncoming': None, 'right': None, 'left': None}, action = right, reward = 12

	Simulator.run(): Trial 9
	Environment.reset(): Trial set up with start = (8, 2), destination = (1, 3), deadline = 40
	Environment.act(): Primary agent has reached destination!
	LearningAgent.update(): deadline = 2, inputs = {'light': 'red', 'oncoming': None, 'right': None, 'left': None}, action = right, reward = 12

As we can see, the agent reached the primary destination 6 out of 10 times.  Moreover, at least in the cases where the destination was reached, the reward was always positive.

## Enhance the driving agent
