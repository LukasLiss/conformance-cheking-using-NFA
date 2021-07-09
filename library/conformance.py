from library.nfa import SpecialActivities, Nfa, Place, PlaceCombined, Transition, TransitionWithCost, trace_check, log_check

def dijkstra_has_unvisited_places(dijkstra_not_visited_places):
    """
    A helping function that checks wether the dijkstra algorithm is already done.

    Parameters
    ----------
    dijkstra_not_visited_places: dictonairy
        a dictonairy that contains a list of not seen inxedes of the trace for each place of a nfa model
    
    Returns
    -------
    bool
        true if there are still places for the dijkstra algorithm to explore, false otherwise.
    """
    for dejure_place in dijkstra_not_visited_places:
        if(len(dijkstra_not_visited_places[dejure_place]) > 0):
            return True
    return False

def optimal_alignment_log_on_nfa(nfa_model, log):
    """
    This function performs dijkstra algorithm on the nfa model and each trace of the log to find the optimal alignment for each trace.

    Parameters
    ----------
    nfa_model : Nfa object
        nfa that describes the behaviour the trace should be aligned to.
    log : list of list of string
        the log that contains all the traces that should be aligned with the model
    
    Returns
    -------
    alignment: list of tuples of string
        The first item of the tuple is move on trace and the second is move on model.
    cost_alignment: integer
        number of not synchronized moves.
    """
    alignments = []
    for trace in log:
        alignments.append(optimal_alignment_trace_on_nfa(nfa_model, trace))
    return alignments

def optimal_alignment_trace_on_nfa(nfa_model, trace):
    """
    This function performs dijkstra algorithm on the nfa model and the trace to find the optimal alignment.

    Parameters
    ----------
    nfa_model : Nfa object
        nfa that describes the behaviour the trace should be aligned to.
    
    trace : list of strings
        the trace that should be aligned with the model
    
    Returns
    -------
    alignment: list of tuples of string
        The first item of the tuple is move on trace and the second is move on model.
    cost_alignment: integer
        number of not synchronized moves.
    """
    input_trace_check_flag = trace_check(trace)
    if not input_trace_check_flag:
        exit()
    infinity = float('inf') # xxx optimize as floats are big in memory
    #initialize
    dijkstra_place_info = {}
    dijkstra_not_visited_places = {} 

    for place in nfa_model.places:
        #no places visited yet
        dijkstra_not_visited_places[place] = []
        for i in range(len(trace) + 1):
            dijkstra_not_visited_places[place].append(i)

        #fill the place info
        for i in range(len(trace)+1): #here the +1 is needed because the index len(trace) represents the end state of the implicit trace nfa
            dijkstra_place_info[(place, i)] = [infinity, None, None] # Format: [cost, predecessor, (ModelMove, LogMove)] - more memory efficient than dict
    #initial cost for start place is 0
    dijkstra_place_info[(nfa_model.start_place, 0)][0] = 0

    #xxx current by old method
    old_not_visited_places = []
    for place in nfa_model.places:
        for i in range(len(trace) + 1):
            old_not_visited_places.append((place, i))

    while (dijkstra_has_unvisited_places(dijkstra_not_visited_places)):

        #select current place (dejureplace and index of trace) that has the lowest cost and was not yet visited
        current_place = None
        current_place_cost = infinity
        current_place_trace_move = None
        for dejure_place in dijkstra_not_visited_places:
                for i in dijkstra_not_visited_places[dejure_place]:
                    if(dijkstra_place_info[(dejure_place, i)][0] < current_place_cost): #lower cost
                        current_place = (dejure_place, i)
                        current_place_cost = dijkstra_place_info[current_place][0]
                        current_place_trace_move = None
                        if(i < len(trace)):
                            current_place_trace_move = trace[i]

        #xxx check wether current_place cost is lower than infinity because otherwise not connected nfa

        #check for all transitions if other places can be reached cheaper
        #- move on log only
        if(current_place[1] < len(trace)):
            log_move_target = (current_place[0], current_place[1]+1)
            log_move_target_cost_via_current_place = dijkstra_place_info[current_place][0] + 1 #the cost of a move on log only is 1
            if(log_move_target_cost_via_current_place < dijkstra_place_info[log_move_target][0]):
                #update dijkstra place info because a cheaper way to a place has been found
                dijkstra_place_info[log_move_target][0] = log_move_target_cost_via_current_place #cost
                dijkstra_place_info[log_move_target][1] = current_place #predecessor
                dijkstra_place_info[log_move_target][2] = (current_place_trace_move, '>>')
                #print("used: ", (current_place_trace_move, '>>'), " to go from ", (current_place[0].label, current_place[1]), " to ",  (log_move_target[0].label, log_move_target[1]), "with cost: ", log_move_target_cost_via_current_place)
        #- move on model only and synchronous moves
        for trans in current_place[0].transitions:
            dejure_transition_target = trans.end_place
            #- move on model only
            model_move_target = (dejure_transition_target, current_place[1])
            model_move_target_cost_via_current_place = dijkstra_place_info[current_place][0] + 1  #the cost of a move on model only is 1
            if(trans.activity == SpecialActivities.EPSILON):
                model_move_target_cost_via_current_place = dijkstra_place_info[current_place][0]  #the cost of a epsilon move on model only is 0
            if(model_move_target_cost_via_current_place < dijkstra_place_info[model_move_target][0]):
                #update dijkstra place info because a cheaper way to a place has been found
                if(trans.activity == SpecialActivities.EPSILON):
                    dijkstra_place_info[model_move_target][0] = model_move_target_cost_via_current_place
                    dijkstra_place_info[model_move_target][1] = current_place #predecessor
                    dijkstra_place_info[model_move_target][2] = None #epsilon moves should not appear in the alignment
                    #print("used: N ", ('>>', trans.activity), " to go from ", (current_place[0].label, current_place[1]), " to ",  (model_move_target[0].label, model_move_target[1]), "with cost: ", model_move_target_cost_via_current_place)
                else:
                    dijkstra_place_info[model_move_target][0] = model_move_target_cost_via_current_place #cost
                    dijkstra_place_info[model_move_target][1] = current_place #predecessor
                    dijkstra_place_info[model_move_target][2] = ('>>', trans.activity)
                    #print("used: ", ('>>', trans.activity), " to go from ", (current_place[0].label, current_place[1]), " to ",  (model_move_target[0].label, model_move_target[1]), "with cost: ", model_move_target_cost_via_current_place)
            #- synchrounous move
            if(current_place[1] < len(trace)):
                if(trans.activity == current_place_trace_move):
                    sync_move_target = (dejure_transition_target, current_place[1]+1)
                    sync_move_target_cost_via_current_place = dijkstra_place_info[current_place][0] #synchronous moves have no cost associated to them
                    if(sync_move_target_cost_via_current_place < dijkstra_place_info[sync_move_target][0]):
                        #update dijkstra place info because a cheaper way to a place has been found
                        dijkstra_place_info[sync_move_target][0] = sync_move_target_cost_via_current_place #cost
                        dijkstra_place_info[sync_move_target][1] = current_place #predecessor
                        dijkstra_place_info[sync_move_target][2] = (trans.activity, current_place_trace_move)
                        #print("used: ", (trans.activity, current_place_trace_move), " to go from ", (current_place[0].label, current_place[1]), " to ",  (sync_move_target[0].label, sync_move_target[1]), "with cost: ", sync_move_target_cost_via_current_place)

        #remove the current selected place from list of not visited places
        dijkstra_not_visited_places[current_place[0]].remove(current_place[1])
    
    #return the alignments along the cheapest path to an accepting place
    #find closest accepting place
    closest_accepting_place = (nfa_model.end_places[0], len(trace)) # xxx there must be an end place in dejure nfa
    cost_to_closest_acc_place = dijkstra_place_info[closest_accepting_place][0]
    for dejure_end_place in nfa_model.end_places:
        if(dijkstra_place_info[(dejure_end_place, len(trace))][0] < cost_to_closest_acc_place):
            closest_accepting_place = (dejure_end_place, len(trace))
            cost_to_closest_acc_place = dijkstra_place_info[closest_accepting_place][0]

    # recreate the path to closest accepting place by going back from closest accepting place to the start place
    alignment = []
    place_we_are_at = closest_accepting_place
    cost_alignment = cost_to_closest_acc_place
    while place_we_are_at != (nfa_model.start_place, 0):
        if(dijkstra_place_info[place_we_are_at][2] != None):
            alignment.insert(0, dijkstra_place_info[place_we_are_at][2]) #insert move that was used to get from predecessor to place we are at
        place_we_are_at = dijkstra_place_info[place_we_are_at][1] #set predecessor to place we are at
    
    return (alignment, cost_alignment)

def is_trace_fitting(nfa_model, trace):

    """
    This function checks if the given trace matches the model. It replays the trace on the model and checks whether it ends up in an accepting end state.

    Parameters
    ----------
    nfa_model : NFA object
        An Nfa describing the wanted behavior, the trace should be aligned to.
    trace : list of str
        activities of a trace/an instance taken from event log.
    
    Returns
    -------
    bool
        true if it matches, false otherwise.

    """

    # trace is here just a list of activities
    # check input

    if (len(trace) == 0):
        if nfa_model.start_place in nfa_model.end_places:
            return True
        # check only for epsilon transitions
        for trans in nfa_model.start_place.transitions:
            if trans.activity == SpecialActivities.EPSILON:
                if (__is_subtrace_fitting(nfa_model, trans.end_place, trace[0:]) == True):
                    return True
        return False

    activity = trace[0]
    for trans in nfa_model.start_place.transitions:
        if trans.activity == activity:
            if (__is_subtrace_fitting(nfa_model, trans.end_place, trace[1:]) == True):
                return True
        if trans.activity == SpecialActivities.EPSILON:
            if (__is_subtrace_fitting(nfa_model, trans.end_place, trace[0:]) == True):
                return True

    return False

def __is_subtrace_fitting(nfa_model, current_place, trace):
    """
    A helping function that checks if the given trace ends up in an accepting end state when started from the current place.

    Parameters
    ----------
    nfa_model : NFA object
        An Nfa describing the wanted behavior, the trace should be aligned to.
    currrent_place: Place object
        place in NFA model that should be used as the initial place to start replaying the trace from
    trace : list of str
        activities of a trace/an instance taken from event log
    
    Returns
    -------
    bool
        true if it matches, false otherwise.
    """
    # trace is here just a list of activities
    # check input

    if (len(trace) == 0):
        if current_place in nfa_model.end_places:
            return True
        # check only for epsilon transitions
        for trans in current_place.transitions:
            if trans.activity == SpecialActivities.EPSILON:
                if (__is_subtrace_fitting(nfa_model, trans.end_place, trace[0:]) == True):
                    return True
        return False

    activity = trace[0]
    for trans in current_place.transitions:
        if trans.activity == activity:
            if (__is_subtrace_fitting(nfa_model, trans.end_place, trace[1:]) == True):
                return True
        if trans.activity == SpecialActivities.EPSILON:
            if (__is_subtrace_fitting(nfa_model, trans.end_place, trace[0:]) == True):
                return True

    return False

def log_fittness(nfa_model, log):
    """
    This function calculates the percentage of perfectly fitting traces in the log (list of traces) when replayed on the NFA model.

    Parameters
    ----------
    nfa_model : NFA object
        An Nfa describing the wanted behavior, the trace should be aligned to.
    log : list of list of strings
        instances/traces taken from event log.
    
    Returns
    -------
    variable: float
        the percentage of perfectly fitting traces.
    """
    # Check for each trace in the log wether the trace is fiting (replayable)
    # return the fraction of traces that are fiting (replayable)
    input_log_check_flag = log_check(log)
    if not input_log_check_flag:
        exit()
    num_fitting_traces = 0
    for trace in log:
        if (is_trace_fitting(nfa_model, trace)):
            num_fitting_traces += 1
    return (num_fitting_traces / len(log))
