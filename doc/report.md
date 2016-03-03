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
two more items to the agent's state:

* light
* next_waypoint

My agent seemed a bit more purposeful at this point.  It did reach the goal several times (with `enforce_deadline` still set to `False`) as I watched it.
