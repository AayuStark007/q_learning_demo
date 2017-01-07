__author__ = 'philippe'
import World
import threading
import time

discount = 0.3
actions = World.actions
states = []
Q = {}
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    """
    Input: The 'action' to be performed.
    Output: s(initial player position), action(that was performed), r(reward{white:-0.04, red:-1, green:1}), s2(final player position)
    
    Description: Performs the 'action' on the player.
    """
    
    s = World.player
    r = -World.score
    
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2


def max_Q(s):
    """
    Input: A tuple contining coords.
    Output: Action(to perform), Score(of that action).
    Data Structure: Q = {(coords): {action:score}}
    
    Description: This function, given the 'coords', iterates over it's actions and finds the action 
    corresponding to the maximum score.
    """    
    
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    """
    Input: s(player position), a(action performed), alpha(learning rate), inc(value by which to increase score for particular s,a pair)
    
    Description: 
    This function learns new score for a given state using the formula: Qnew <- Qold + alpha*((reward + discount * Qest) - Qold), 
    where, (reward + discount * Qest) is the learning rate represented by 'inc' and Qest is the estimated(future) value of Q.
    Here, the formula is written as Q = Q(1-alpha) * (alpha*inc) in two steps which is same as the formula given above.
    """
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])


def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    while True:
        # Pick the right action
        s = World.player

        max_act, max_val = max_Q(s)
        
        (s, a, r, s2) = do_action(max_act)

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.05)


def printQ(struct):
    for elem in struct:
        print(elem)
        print(struct[elem])
        #print(d)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
