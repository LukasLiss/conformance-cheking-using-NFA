class SpecialActivities:
    """
    This class is the collection of special characters used in regular expressions.

    Attributes
    ----------
    Epsilon: str
        stores the value of epsilon

    """

    EPSILON = '\u03B5'


class Place:
    """
    This class represents a place in NFA.

    Attributes
    ----------
    label : str
        name of the node / place
    transitions: list of str
        collection of transition to other places

    Methods
    -------
    __init__ : constructor
       sets the string passed as label (place) of that instance and initializes the transitions list.

    """

    def __init__(self, label):
        """
        Constructor of class Place.

        Parameters
        ----------
        label : str
            any label passed by the user is set in this variable
        transitions: list of str
            collection of transitions to other places

        Returns
        -------
        None.

        """
        self.label = label
        self.transitions = []

class PlaceCombined(Place):
    def __init__(self, label):
        """
        Constructor of class Place.

        Parameters
        ----------
        label : str
            any label passed by the user is set in this variable
        transitions: list of str
            collection of transitions to other places

        Returns
        -------
        None.

        """
        super().__init__(label)
        self.model_place = None
        self.trace_place = None


class Transition:
    """
    This class represents transition / edge in NFA model.

    Attributes
    ----------
    activity: str 
        the event that needs to happen in order to transition from start to end place
    start_place: str
        connected start place of the transition 
    end_place: str
        end place where the transition leads to

    Methods
    -------
    __init__ : constructor
       sets the values of activity, start place of the activity and its end place.

    """

    def __init__(self, activity, start_place, end_place):
        """
        Constructor of class Transition that sets values of the instance.

        Parameters
        ----------
        activity : str
            alphabet reflecting one activity of the instance from event log
        start_place : str
            start state of the activity at hand.
        end_place : str
            end state of the activity at hand.

        Returns
        -------
        None.

        """
        self.activity = activity
        self.start_place = start_place
        self.end_place = end_place

class TransitionWithCost(Transition):
    def __init__(self, activity, start_place, end_place, cost, alignment_element):
        super().__init__(activity, start_place, end_place)
        self.cost = cost
        self.alignment_element = alignment_element

class Nfa:
    """
    This class represents the NFA model. It also provides the function that checks the fitness of a log based on NFA model.

    Attributes
    ----------
    label : str
        name of NFA
    places : list of str
        all the places the NFA contains
    start_place : str
        the place that is the initial place when the NFA model is initialized. (Default: None)
    end_places : list of str
        accepted end places in NFA

    Methods
    -------
    __init__ : constructor
       initialize the attributes and sets the label passed during instance creation.
    
    """

    def __init__(self, label):
        """
        Initializes the attributes and sets the label passed during instance creation.

        Parameters
        ----------
        label : str
            name of NFA
        places : list of str
            all the places the NFA contains
        transitions : list of str
            collection of transitions to other places
        start_place : str
            the place that is the initial place when the NFA model is initialized. (Default: None)
        end_places : list of str
            accepted end places in NFA        

        Returns
        -------
        None.

        """
        self.label = label
        self.places = []
        self.transitions = []
        self.start_place = None  # here we use the definiton of an NFA with just one start place
        self.end_places = []  # but multiple acepting end places

    def print(self):
        """
        This function prints the NFA model.

        Parameters
        ----------
        None.   

        Returns
        -------
        None.

        """
        print("Start place: " + self.start_place.label + str(self.places.index(self.start_place)))
        for place in self.places:
            print("Place: " + place.label + "_" + str(self.places.index(place)))
            if place in self.end_places:
                print("Endplace")
            for trans in place.transitions:
                print("" + trans.start_place.label + "_" + str(self.places.index(
                    trans.start_place)) + " - " + trans.activity + " - " + trans.end_place.label + "_" + str(
                    self.places.index(trans.end_place)))

    def add_place(self, place, is_start_place=False, is_end_place=False):
        """
        It adds a place to the existing NFA model. If start and end place values are not given in second and third argument, they are by default taken to be False.

        Parameters
        ----------
        place : Place object
            the place that will be added to the NFA
        is_start_Place : bool
            to set/define whether its the start place. (Default: False)
        is_end_Place : bool
            to set/define whether its the end place. (Default: False)

        Returns
        -------
        None.

        """
        # check whether place is a Place

        # check whether place allready exist
        self.places.append(place)
        if is_start_place and (self.start_place is None):
            # check whether allready a start place is defined
            self.start_place = place
        if is_end_place:
            self.end_places.append(place)

    def remove_place(self, place):
        """
        This function removes a place from the NFA model.

        Parameters
        ----------
        place : Place object
            the place that needs to be removed from the NFA model. 

        Returns
        -------
        None.
        """
        # check whether place is a Place

        self.places.remove(place)

    def add_Transition(self, transition):
        """
        This function adds a transition to the existing NFA model.

        Parameters
        ----------
        transition : Transition object
            it is the transition that will be added.
        
        Returns
        -------
        None.

        """
        # check whether transition is a Transition
        # check whether transition only has places that exist
        # check for duplicate
        for place in self.places:
            if place == transition.start_place:
                place.transitions.append(transition)
                break

    def remove_Transition(self, transition):
        """
        This function removes a transition from the NFA model.

        Parameters
        ----------
        transition : Transition object
            the transition that is required to be removed from the NFA model.
        
        Returns
        -------
        None.

        """
        # input checks
        for place in self.places:
            if place == transition.start_place:
                place.transitions.remove(transition)
                break

    def is_fitting(self, trace):

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
            if self.start_place in self.end_places:
                return True
            # check only for epsilon transitions
            for trans in self.start_place.transitions:
                if trans.activity == SpecialActivities.EPSILON:
                    if (self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True):
                        return True
            return False

        activity = trace[0]
        for trans in self.start_place.transitions:
            if trans.activity == activity:
                if (self.__is_subtrace_fitting(trans.end_place, trace[1:]) == True):
                    return True
            if trans.activity == SpecialActivities.EPSILON:
                if (self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True):
                    return True

        return False

    def __is_subtrace_fitting(self, current_place, trace):
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
            if current_place in self.end_places:
                return True
            # check only for epsilon transitions
            for trans in current_place.transitions:
                if trans.activity == SpecialActivities.EPSILON:
                    if (self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True):
                        return True
            return False

        activity = trace[0]
        for trans in current_place.transitions:
            if trans.activity == activity:
                if (self.__is_subtrace_fitting(trans.end_place, trace[1:]) == True):
                    return True
            if trans.activity == SpecialActivities.EPSILON:
                if (self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True):
                    return True

        return False

    def log_fittness(self, log):
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
            if (self.is_fitting(trace)):
                num_fitting_traces += 1
        return (num_fitting_traces / len(log))

    def compute_alignments(self, log):
        alignments = []
        for trace in log:
            alignments.append(self.align_trace(trace))
        return alignments

    def align_trace(self, trace):
        if self.is_fitting(trace):
            #create a perfectly fitting alignment
            al = []
            for event in trace:
                al.append((event, event))
            return al

        # for not fittin traces calculate alignment
        #create the combined nfa
        combined_nfa = self.construct_combined_nfa(trace)

        #search for shortest path on the combined nfa using dijkstra
        alignment, cost = self.dijkstra_on_combined_nfa(combined_nfa)
        return (alignment, cost)

    def dijkstra_on_combined_nfa(self, comb_nfa):
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
            cost_current_place = self.dijkstra_info_of_place(place_info_list, current_place)[1]
            for place in not_visited_places: # xxx optimize - too many iterations over the lists
                # check for smaller cost
                help_cost = self.dijkstra_info_of_place(place_info_list, place)[1]
                if(help_cost < cost_current_place):
                    current_place = place
                    cost_current_place = self.dijkstra_info_of_place(place_info_list, current_place)[1]

            #check for all transitions if other places can be reached cheaper
            for trans in current_place.transitions:
                transition_target = trans.end_place
                cost_over_current_to_target = cost_current_place + trans.cost
                if(cost_over_current_to_target < self.dijkstra_info_of_place(place_info_list, transition_target)[1]):
                    #cheaper way found - add to info list
                    info_target = self.dijkstra_info_of_place(place_info_list, transition_target)
                    info_target[1] = cost_over_current_to_target
                    info_target[2] = current_place
                    info_target[3] = trans.alignment_element

            #remove the current selected place from list of not visited places
            not_visited_places.remove(current_place)
        
        #return the alignments along the cheapest path to an accepting place
        #find closest accepting place
        closest_accepting_place = comb_nfa.end_places[0] # xxx there must be an end place
        cost_to_closest_acc_place = self.dijkstra_info_of_place(place_info_list, closest_accepting_place)[1]
        for acc_place in comb_nfa.end_places:
            if self.dijkstra_info_of_place(place_info_list, acc_place)[1] < cost_to_closest_acc_place:
                closest_accepting_place = acc_place
                cost_to_closest_acc_place = self.dijkstra_info_of_place(place_info_list, closest_accepting_place)[1]
        # recreate the path to closest accepting place by going back from closest accepting place to the start place
        #xxx hier the cost of the alignment can also be added up
        alignment = []
        place_we_are_at = closest_accepting_place
        cost_alignment = self.dijkstra_info_of_place(place_info_list, place_we_are_at)[1]
        while place_we_are_at != comb_nfa.start_place:
            info_we_are_at = self.dijkstra_info_of_place(place_info_list, place_we_are_at)
            alignment.insert(0, info_we_are_at[3])
            place_we_are_at = info_we_are_at[2]
        
        return (alignment, cost_alignment)



    def dijkstra_info_of_place(self, info_list, place):
        for info in info_list:
            if(info[0] == place):
                return info
        return None


    def construct_combined_nfa(self, trace):
        trace_nfa = nfa_from_trace(trace)
        
        combined_nfa = Nfa("combined")
        # create all combined places
        for trace_place in trace_nfa.places:
            for model_place in self.places:
                comb_place = PlaceCombined(trace_place.label + "+" + model_place.label)
                comb_place.trace_place = trace_place
                comb_place.model_place = model_place
                # check for combined start and end places
                is_start = False
                if((trace_place == trace_nfa.start_place) and (model_place == self.start_place)):
                    is_start = True
                is_end = False
                if((trace_place in trace_nfa.end_places) and (model_place in self.end_places)):
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

def nfa_from_trace(trace):
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

        

def convert_from_regex(regex):
    """
    Fucntion that creates and returns the NFA based on the given regular expression.

    Parameters
    ----------
    regex : list of characters
        regular expressions that will be converted to NFA model.

    Returns
    -------
    NFA : NFA object
        the final model that describes the same accepted language as regular expression.
    """
    return expression(regex)


# Grammer used to describe the accepted regular expression:
# Expression := Konkat { "|" Konkat}
# Konkat := Prod {(".", "") Prod}  - until now the . is a must
# Prod := Factor ("*", "")
# Factor := Activity | "(" Expression ")"
# Activity := "a" | "b" | ... (all letters)

def expression(regex):
    """
    Fucntion that returns the NFA model defined by the regular expression interpreted as expression part, defined by the used regular expression grammar which is as follows:
    Expression := Konkat { "|" Konkat}
    Konkat := Prod {(".", "") Prod}  - until now the . is a must
    Prod := Factor ("*", "")
    Factor := Activity | "(" Expression ")"
    Activity := "a" | "b" | ... (all letters)

    Parameters
    ----------
    regex : list of characters
        regular expressions that will be converted to NFA model

    Returns
    -------
    NFA : NFA object
        the model that describe the same accepted language as regular expression
    """

    list_of_konkats = []
    list_of_konkats.append(konkat(regex))
    while (len(regex) > 0 and regex[0] == "|"):
        regex.pop(0)
        list_of_konkats.append(konkat(regex))
    return (unite_nfas(list_of_konkats))


def konkat(regex):
    """
    It returns the NFA model defined by the regular expression interpreted as a concatenation part.

    Parameters
    ----------
    regex : list of characters
        regular expressions that will be converted to NFA model

    Returns
    -------
    NFA : NFA object
        returns the NFA model defined by the regular expression interpreted as a concatenation part
    """
    list_of_prods = []
    list_of_prods.append(prod(regex))
    while (len(regex) > 0 and regex[0] == "."):
        regex.pop(0)
        list_of_prods.append(prod(regex))
    return konkatonate_nfas(list_of_prods)


def prod(regex):
    """
    It returns the NFA model defined by the regular expression interpreted as a product(* operator) part.

    Parameters
    ----------
    regex : list of characters
        regular expressions that will be converted to NFA model

    Returns
    -------
    NFA : NFA object
        returns the NFA model defined by the regular expression interpreted as a product(* operator) part
    """
    factor_nfa = factor(regex)
    if (len(regex) > 0 and regex[0] == "*"):
        regex.pop(0)
        return star_nfa(factor_nfa)
    return (factor_nfa)


def factor(regex):
    """
    It represents the grammar rule "factor" as mentioned above. It returns the NFA model defined by the regular expression interpreted as a factor part. It detects the paranthesis.

    Parameters
    ----------
    regex : list of characters
        regular expressions that will be converted to NFA model

    Returns
    -------
    NFA : NFA object
        returns the NFA model defined by the regular expression interpreted as factor part.
    """
    # testing push
    if (len(regex) > 0 and regex[0].isalpha()):
        activity = regex.pop(0)
        activity_nfa = nfa_from_activity(activity)
        return activity_nfa
    if (len(regex) > 0 and regex[0] == "("):
        regex.pop(0)
        sub_nfa = expression(regex)
        if (len(regex) > 0 and regex[0] != "("):
            print("Error: Was expecting a closing parenthesis but recived: " + regex[0])
        regex.pop(0)
        return sub_nfa


# helping functions
def unite_nfas(nfas):
    """
    It creates a NFA that accepts the combination (| operator) of given NFAs based on thomson construction.

    Parameters
    ----------
    nfas : list of Nfa
        list of nfa models that will be combined

    Returns
    -------
    united_nfa: NFA object
        the final nfa after consolidation of nfas in the given list of NFAs
    """
    if (len(nfas) == 1):
        return nfas[0]

    united_nfa = Nfa("unite")
    p_start = Place("u_s")
    united_nfa.add_place(p_start, True)
    p_end = Place("u_e")
    united_nfa.add_place(p_end, False, True)
    for nfa in nfas:
        # add places with their transitions
        for place in nfa.places:
            united_nfa.add_place(place)
        # connect the united start place to the start place of the nfa
        united_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, nfa.start_place))
        # connect all accepting places to the united accepting place
        for acc_place in nfa.end_places:
            united_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, p_end))
    return united_nfa


def konkatonate_nfas(nfas):
    """
    It creates a NFA that accepts the combination (. operator; placing one NFA after another NFA) of given NFAs based on thomson construction.

    Parameters
    ----------
    nfas : list of Nfa
        list of nfa models that will be combined

    Returns
    -------
    konkat_nfa: NFA object
        the final nfa after concatenation of nfas in the given list of NFAs
    """

    if (len(nfas) == 1):
        return nfas[0]

    konkat_nfa = Nfa("konkat")
    p_start = Place("k_s")
    konkat_nfa.add_place(p_start, True)
    p_end = Place("k_e")
    konkat_nfa.add_place(p_end, False, True)
    for nfa in nfas:
        # add places with their transitions
        for place in nfa.places:
            konkat_nfa.add_place(place)
    # connect the accepting places of each nfa in the list to the start place of the following nfa  ---- optimisation potential by not going through the nfas twice
    for i in range(len(nfas) - 1):
        for acc_plac in nfas[i].end_places:
            konkat_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_plac, nfas[i + 1].start_place))

    # add Transition from new start to start of first nfa in list
    konkat_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, nfas[0].start_place))
    # add Transition from last nfa in list to new last place
    for acc_place in nfas[len(nfas) - 1].end_places:
        konkat_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, p_end))

    return konkat_nfa


def star_nfa(nfa):
    """
    It creates a NFA that accepts the combination (* operator) of given NFAs based on thomson construction.

    Parameters
    ----------
    nfa : list of Nfa
        any NFA

    Returns
    -------
    star_nfa: NFA object
        NFA that accepts the language of the given nfa after applying the * operator on the given NFA.
    """
    star_nfa = Nfa("star")
    p_start = Place("s_s")
    star_nfa.add_place(p_start, True)
    p_end = Place("s_e")
    star_nfa.add_place(p_end, False, True)

    # add all places from nfa
    for place in nfa.places:
        star_nfa.add_place(place)

    # one can skip the nfa
    star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, p_end))
    # connect new start to the start of the nfa
    star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, nfa.start_place))
    # connect new end to the start of the nfa
    star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_end, nfa.start_place))

    # connect accepting places of the nfa to the new end place
    for acc_place in nfa.end_places:
        star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, p_end))

    return star_nfa


def nfa_from_activity(activity):
    """
    It gets an activity from the event log. For a given activity it retuens the NFA that accpets only this activity. This is the base case for the thomson construction.

    Parameters
    ----------
    activty : char
        character that represents an activity from the event log

    Returns
    -------
    base_nfa: NFA object
        the nfa model accepting just the given acitivity from the log.
    """
    base_nfa = Nfa("activity")
    p_start = Place("a_s")
    base_nfa.add_place(p_start, True)
    p_end = Place("a_e")
    base_nfa.add_place(p_end, False, True)
    base_nfa.add_Transition(Transition(activity, p_start, p_end))
    return base_nfa


def trace_check(trace):
    if not isinstance(trace, list):
        print("Input is not a list")
        return False
    for i in trace:
        if not i.isalnum():
            print("Only alphanumeric values are allowed")
            return False
        if i.isalnum and not len(i) == 1:
            print("Only single characters are allowed")
            return False

    return True

def re_expression_check(trace):
    special_characters = ["+", "*", "|", ".", "(", ")","-"]
    count1 = 0

    if not isinstance(trace, list):
        print("Input is not a list")
        return False
    for i in trace:
        if (i.isalnum() or i in special_characters) and not len(i) == 1:
            print("Only single characters are allowed")
            return False

        if not i.isalnum() and i not in special_characters:
            print("Only alphanumeric values with given set of special characters [ + | * . ( ) ] are allowed")
            return False
        if i == "(":
            count1 += 1
        if i == ")" :
            count1 -= 1
        if count1 < 0:
            print("Invalid Expression: Missing opening bracket")
            return False
    if count1 != 0:
        print("Invalid Expression: Closing bracket not found")
        return False
    return True

# Test section

myNFA = Nfa("TestNFA")
p1 = Place("Greating")
myNFA.add_place(p1, True)
p2 = Place("Start Small Talk")
myNFA.add_place(p2)
p3 = Place("End Small Talk")
myNFA.add_place(p3)
p4 = Place("Good Bye")
myNFA.add_place(p4, False, True)
t1 = Transition("a", p1, p2)
myNFA.add_Transition(t1)
t2 = Transition("b", p2, p2)
myNFA.add_Transition(t2)
t3 = Transition("b", p2, p3)
myNFA.add_Transition(t3)
t4 = Transition("c", p3, p4)
myNFA.add_Transition(t4)

print(myNFA.places)
# print(myNFA.transitions)
#
# print(myNFA.is_fitting(["a", "b", "c"]))  # True
# print(myNFA.is_fitting(["a", "b", "b", "b", "c"]))  # True
# print(myNFA.is_fitting(["a", "a", "b", "c"]))  # False
# print(myNFA.is_fitting(["a", "c"]))  # False
# print(myNFA.is_fitting(["a", "b"]))  # False
#
# myNFA.add_Transition(Transition(SpecialActivities.EPSILON, p2, p4))
#
# print(myNFA.is_fitting(["a"]))  # True
#
# myRegexNfa = expression(["a", "*", "|", "(", "c", ".", "d", ")", "|", "(", "e", ".", "f", ")"])
# myRegexNfa.print()
#
# print("Regex: ")
# print(myRegexNfa.is_fitting(["a", "a"]))  # True
# print(myRegexNfa.is_fitting(["a"]))  # True
# print(myRegexNfa.is_fitting([]))  # True
# print(myRegexNfa.is_fitting(["c", "d"]))  # True
# print(myRegexNfa.is_fitting(["e", "f"]))  # True
# print(myRegexNfa.is_fitting(["a", "c"]))  # False
# print(myRegexNfa.is_fitting(["a", "c", "d"]))  # False
# print(myRegexNfa.is_fitting(["x"]))  # False
# print(myRegexNfa.is_fitting(["c"]))  # False

# nfa from trace test
# myTrace = ["a", "b", "b", "b", "c", "z"]
# myOtherTrace = ["a", "b"]
# myNfa = nfa_from_trace(myTrace)
# print(myNfa.is_fitting(myTrace)) # True
# print(myNfa.is_fitting(myOtherTrace)) # False

# combined nfa test
myTrace = ["a", "b", "b", "b", "c", "z"]
#print(myNFA.construct_combined_nfa(myTrace))
print(myNFA.align_trace(myTrace))
myTrace = ["a", "z", "b", "b", "c"]
print(myNFA.align_trace(myTrace))
myTrace = ["a", "z", "b", "b"]
print(myNFA.align_trace(myTrace))