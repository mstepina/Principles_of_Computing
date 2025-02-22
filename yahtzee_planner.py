"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """   
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Computes the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    score_list = []
    for die in hand:
        count = hand.count(die)
        score_list.append(die*count)
    return max(score_list)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Computes the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    rest_rolls = gen_all_sequences(range(1,num_die_sides+1), num_free_dice)
    all_scores = 0 
    for roll in rest_rolls:
        all_scores += score(held_dice + roll)
    return float(all_scores) / len(rest_rolls)    
    

def gen_all_holds(hand):
    """
    Generates all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """ 
    
    result_set = set([()])
    
    copy_hand = list(hand)
    for num in copy_hand:
        temp_set = set([()])
        for elem in result_set:
            new_seq = list(elem)
            new_seq.append(num)
            temp_set.add(tuple(new_seq))
        result_set = result_set.union(temp_set)
    return result_set    


def strategy(hand, num_die_sides):
    """
    Computes the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    winning = [0.0,0]
    for hold_var in gen_all_holds(hand):
        exp_val = expected_value(hold_var, num_die_sides,(len(hand) - len(hold_var)))
        if exp_val > winning[0]:
            winning[0] = exp_val
            winning[1]= hold_var
    return (winning[0], winning[1])


def run_example():
    """
    Computes the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1,1,1,5,6)    
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                      
