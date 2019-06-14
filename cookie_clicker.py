"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 10000.0

class ClickerState:
    """
    Class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0,None,0.0,0.0)]
        
    def __str__(self):
        """
        Returns human readable state
        """
        return ("Total cookies: " + str(self._total_cookies)+
                ". \nCurrent cookies: " + str(self._current_cookies) + 
                ". \nCurrent CPS: " + str(self._current_cps) + 
                ". \nCurrent time: " + str(self._current_time))
     
    def get_cookies(self):
        """
        Returns current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Gets current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Gets current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Returns history list

        a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Returns time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            return 0.0
        cookies_left = cookies - self._current_cookies
        return math.ceil(cookies_left/self._current_cps)
          
    def wait(self, time):
        """
        Waits for given amount of time and updates state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_time += time
            self._total_cookies += time * self._current_cps
            self._current_cookies += time * self._current_cps
               
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buys an item and updates state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost,self._total_cookies))
        
      
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    info = build_info.clone()
    new_clicker = ClickerState() 
    while new_clicker.get_time() <= duration:
        if new_clicker.get_time() > duration:
            break
        left_time = duration - new_clicker.get_time()    
        strateg_item = strategy (new_clicker.get_cookies(), new_clicker.get_cps(), 
                  new_clicker.get_history(), left_time, info)
        if strateg_item == None:
            break
        time_elapse = new_clicker.time_until(info.get_cost(strateg_item))
        if time_elapse > left_time:
            break
        else:
            new_clicker.wait(time_elapse)
            while new_clicker.get_cookies() >= info.get_cost(strateg_item):
                new_clicker.buy_item(strateg_item, info.get_cost(strateg_item),
                             info.get_cps(strateg_item))
                info.update_item(strateg_item)    
    new_clicker.wait(left_time)
    return new_clicker    
            

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    This simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.
    """   
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    helps to debug simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """    
    cookies += time_left * cps   
    cheapest_price = float('inf')
    cheapest_item = None
    for item in build_info.build_items(): 
        cost_item = build_info.get_cost(item)
        if (cost_item < cheapest_price) and (cost_item <= cookies):
            cheapest_price = cost_item
            cheapest_item = item        
    return cheapest_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """    
    cookies += time_left * cps
    most_price = 0.0
    items  = build_info.build_items()
    most_item = None
    for item in items:  
        cost_item = build_info.get_cost(item)
        if  (cost_item <= cookies) and (cost_item > most_price) :
            most_price = cost_item
            most_item = item
    return most_item
    

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy.
    """
    cookies += time_left * cps
    best_ratio = 0.0
    best_option = None
    items  = build_info.build_items()
    for item in items:
        cost_item = build_info.get_cost(item)
        if cookies >= cost_item: 
            ratio = build_info.get_cps(item) / cost_item
            if ratio > best_ratio:
                best_ratio = ratio
                best_option = item
    return best_option            
        
           
def run_strategy(strategy_name, time, strategy):
    """
    Simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time
    history = state.get_history()
    print history
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

    
def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)    
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)    
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
