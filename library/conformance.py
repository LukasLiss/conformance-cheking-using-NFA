from library.nfa import SpecialActivities, Nfa, Place, PlaceCombined, Transition, TransitionWithCost

def dijkstra_has_unvisited_places(dijkstra_not_visited_places):
    for dejure_place in dijkstra_not_visited_places:
        if(len(dijkstra_not_visited_places[dejure_place]) > 0):
            return True
    return False

def optimal_alignment_log_on_nfa(nfa_model, log):
    alignments = []
    for trace in log:
        alignments.append(optimal_alignment_trace_on_nfa(nfa_model, trace))
    return alignments

def optimal_alignment_trace_on_nfa(nfa_model, trace):
    """
    This function performs dijkstra algorithm on the dejure nfa and the trace to find the optimal alignment.

    Parameters
    ----------
    nfa_model : Nfa object
        nfa that consists of places of type PlaceCombined and transitions with cost associated with them.
    
    Returns
    -------
    alignment: list of tuples of string
        The first item of the tuple is move on trace and the second is move on model.
    cost_alignment: integer
        number of not synchronized moves.
    """
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
    This function checks if the given trace mathces the model. It replays the trace on the model and checks whether it ends up in an accepting end state.

    Parameters
    ----------
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
    log : list of list of strings
        instances/traces taken from event log.
    
    Returns
    -------
    variable: float
        the percentage of perfectly fitting traces.
    """
    # Check for each trace in the log wether the trace is fiting (replayable)
    # return the fraction of traces that are fiting (replayable)
    num_fitting_traces = 0
    for trace in log:
        if (is_trace_fitting(nfa_model, trace)):
            num_fitting_traces += 1
    return (num_fitting_traces / len(log))


################################### OLD VERSION ##################################

def compute_alignments(dejure, log): # done
    """
    This function computes optimal alignments for each trace of the given log.

    Parameters
    ----------
    log : list of list of strings
        instances/traces taken from event log.
    
    Returns
    -------
    alignments: list of list of tuples of strings
        list of alignments where each alignmeent is represented by a list of tuples. The first item of the tuple is the move on the trace and the second item is the move on model.
    """
    alignments = []
    for trace in log:
        alignments.append(align_trace(dejure, trace))
    return alignments

def align_trace(dejure, trace): #done
    """
    This function calculates the alignment for the given trace.

    Parameters
    ----------
    trace : list of strings
        instance taken from event log.
    
    Returns
    -------
    alignment: list of tuples of strings
        The first item of the tuple is move on trace and the second item is move on model.
    cost: integer
        number of not synchronized moves.
    """
    if calculate_fitness(dejure, trace):
        #create a perfectly fitting alignment
        al = []
        for event in trace:
            al.append((event, event))
        return al

    # for not fittin traces calculate alignment
    #create the combined nfa
    combined_nfa = construct_combined_nfa(dejure, trace)

    #search for shortest path on the combined nfa using dijkstra
    alignment, cost = dijkstra_on_combined_nfa(dejure, combined_nfa)
    return (alignment, cost)

def dijkstra_on_combined_nfa(dejure, comb_nfa):  #done
    """
    This function performs dijkstra algorithm on comb_nfa to find the optimal alignment.

    Parameters
    ----------
    comb_nfa : Nfa object
        nfa that consists of places of type PlaceCombined and transitions with cost associated with them.
    
    Returns
    -------
    alignment: list of tuples of string
        The first item of the tuple is move on trace and the second is move on model.
    cost_alignment: integer
        number of not synchronized moves.
    """
    infinity = float('inf') # xxx optimize as floats are big in memory
    #initialize
    place_info_list = []
    not_visited_places = [] #(place, actual lowest cost, place from which it was reached, transition alignment with which it was reached)
    for place in comb_nfa.places:
        not_visited_places.append(place)
        if place == comb_nfa.start_place:
            place_info_list.append([place, 0, None, None])
        else:
            place_info_list.append([place, infinity, None, None])

    #search until shortest path for each node found
    while (len(not_visited_places) > 0):
        #select current not that has the lowest cost and was not yet visited
        current_place = not_visited_places[0]
        cost_current_place = dijkstra_info_of_place(place_info_list, current_place)[1]
        for place in not_visited_places: # xxx optimize - too many iterations over the lists
            # check for smaller cost
            help_cost = dijkstra_info_of_place(place_info_list, place)[1]
            if(help_cost < cost_current_place):
                current_place = place
                cost_current_place = dijkstra_info_of_place(place_info_list, current_place)[1]

        #check for all transitions if other places can be reached cheaper
        for trans in current_place.transitions:
            transition_target = trans.end_place
            cost_over_current_to_target = cost_current_place + trans.cost
            if(cost_over_current_to_target < dijkstra_info_of_place(place_info_list, transition_target)[1]):
                #cheaper way found - add to info list
                info_target = dijkstra_info_of_place(place_info_list, transition_target)
                info_target[1] = cost_over_current_to_target
                info_target[2] = current_place
                info_target[3] = trans.alignment_element

        #remove the current selected place from list of not visited places
        not_visited_places.remove(current_place)
    
    #return the alignments along the cheapest path to an accepting place
    #find closest accepting place
    closest_accepting_place = comb_nfa.end_places[0] # xxx there must be an end place
    cost_to_closest_acc_place = dijkstra_info_of_place(place_info_list, closest_accepting_place)[1]
    for acc_place in comb_nfa.end_places:
        if dijkstra_info_of_place(place_info_list, acc_place)[1] < cost_to_closest_acc_place:
            closest_accepting_place = acc_place
            cost_to_closest_acc_place = dijkstra_info_of_place(place_info_list, closest_accepting_place)[1]
    # recreate the path to closest accepting place by going back from closest accepting place to the start place
    #xxx hier the cost of the alignment can also be added up
    alignment = []
    place_we_are_at = closest_accepting_place
    cost_alignment = dijkstra_info_of_place(place_info_list, place_we_are_at)[1]
    while place_we_are_at != comb_nfa.start_place:
        info_we_are_at = dijkstra_info_of_place(place_info_list, place_we_are_at)
        alignment.insert(0, info_we_are_at[3])
        place_we_are_at = info_we_are_at[2]
    
    return (alignment, cost_alignment)


def dijkstra_info_of_place(info_list, place): #done
    """
    A helper function which returns information stored by the dijkstra algo for the given place. 

    Parameters
    ----------
    info_list : list of lists
        list of information about places that dijkstra algo has created so far.
    place : Place object
        the place one is interested in getting the information about.
    
    Returns
    -------
    info: list
        a list containing the place as first element, cost as the second element, previous place in the shortest path as the third element and alignment used to go to the given place as the fourth element.
    """
    for info in info_list:
        if(info[0] == place):
            return info
    return None


def construct_combined_nfa(dejure, trace):  #done
    """
    This function returns/creates an nfa that simulates a parallel execution of the nfa and an nfa that only accepts the given trace.

    Parameters
    ----------
    trace : list of strings
        instance taken from event log.
    
    Returns
    -------
    combined_nfa: Nfa object
        nfa that simulates a parallel execution of the nfa and an nfa that only accepts the given trace.
    """
    trace_nfa = nfa_from_trace(trace)
    
    combined_nfa = Nfa("combined")
    # create all combined places
    for trace_place in trace_nfa.places:
        for model_place in dejure.places:
            comb_place = PlaceCombined(trace_place.label + "+" + model_place.label)
            comb_place.trace_place = trace_place
            comb_place.model_place = model_place
            # check for combined start and end places
            is_start = False
            if((trace_place == trace_nfa.start_place) and (model_place == dejure.start_place)):
                is_start = True
            is_end = False
            if((trace_place in trace_nfa.end_places) and (model_place in dejure.end_places)):
                is_end = True
            combined_nfa.add_place(comb_place, is_start, is_end)
    
    # find all transitions that are possible
    #add transitions that are synchronized moves
    for place in combined_nfa.places: #xxx This loop can be combined with one above for performance increase
        for trans_trace in place.trace_place.transitions:
            for trans_model in place.model_place.transitions:
                if(trans_trace.activity != trans_model.activity):
                    continue
                goal_place_trace = trans_trace.end_place
                goal_place_model = trans_model.end_place
                #find the goal place in the combined nfa (it is the one that has both goal states as the connected places)
                goal_place_combined = None
                for comb_place in combined_nfa.places:
                    if ((comb_place.model_place == goal_place_model) and (comb_place.trace_place == goal_place_trace)):
                        goal_place_combined = comb_place
                        break

                # calculate cost of transition based on wether it is a synchronous move or not
                cost = 1
                if(trans_trace.activity == trans_model.activity):
                    cost = 0

                # add transition in the combined nfa
                align_elem = (trans_trace.activity, trans_model.activity)
                comb_transition = TransitionWithCost(trans_trace.activity + "|" + trans_model.activity, place, goal_place_combined, cost, align_elem)
                combined_nfa.add_Transition(comb_transition)

    #add transitions that are model moves only
    for place in combined_nfa.places: #xxx This loop can be combined with one above for performance increase
        for trans_model in place.model_place.transitions:
                goal_place_trace = place.trace_place # stays the same because only move on model
                goal_place_model = trans_model.end_place
                #find the goal place in the combined nfa (it is the one that has both goal states as the connected places)
                goal_place_combined = None
                for comb_place in combined_nfa.places:
                    if ((comb_place.model_place == goal_place_model) and (comb_place.trace_place == goal_place_trace)):
                        goal_place_combined = comb_place
                        break

                # cost of a model move only
                cost = 1

                # add transition in the combined nfa
                align_elem = (">>", trans_model.activity)
                comb_transition = TransitionWithCost(">>"+ "|" + trans_model.activity, place, goal_place_combined, cost, align_elem)
                combined_nfa.add_Transition(comb_transition)

    #add transitions that are trace moves only
    for place in combined_nfa.places: #xxx This loop can be combined with one above for performance increase
        for trans_trace in place.trace_place.transitions:
                goal_place_trace = trans_trace.end_place # stays the same because only move on model
                goal_place_model = place.model_place
                #find the goal place in the combined nfa (it is the one that has both goal states as the connected places)
                goal_place_combined = None
                for comb_place in combined_nfa.places:
                    if ((comb_place.model_place == goal_place_model) and (comb_place.trace_place == goal_place_trace)):
                        goal_place_combined = comb_place
                        break

                # cost of a trace move only
                cost = 1

                # add transition in the combined nfa
                align_elem = (trans_trace.activity, ">>")
                comb_transition = TransitionWithCost(trans_trace.activity + "|" + ">>", place, goal_place_combined, cost, align_elem)
                combined_nfa.add_Transition(comb_transition)
    
    return combined_nfa

def nfa_from_trace(trace):  #done
    """
    This function creates an nfa that only accepts the given trace.

    Parameters
    ----------
    trace : list of strings
        instance taken from event log.

    Returns
    -------
    trace_nfa : NFA object
        nfa that only accepts the given trace.
    """
    #xxx empty traces are not supported
    trace_nfa = Nfa("trace_nfa")
    p_start = Place("t_s")
    trace_nfa.add_place(p_start, True)
    p_end = Place("t_e")
    trace_nfa.add_place(p_end, False, True)

    # add all the transistions to accept only the trace as the language of the nfa
    current_place = p_start
    for ev_i in range(len(trace)-1): #xxx check what happens when len = 0 and then -1
        p_help = Place("t_" + str(ev_i))
        trace_nfa.add_place(p_help)
        trans = Transition(trace[ev_i], current_place, p_help)
        trace_nfa.add_Transition(trans)
        current_place = p_help
    trans = Transition(trace[len(trace)-1], current_place, p_end)
    trace_nfa.add_Transition(trans)
    return trace_nfa