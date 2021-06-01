class SpecialActivities:
    EPSILON = '\u03B5'

class Place:
    """
    This class sets the label of the instance.

    Attributes
    ----------
    None.

    Methods
    -------
    __init__ : constructor
       sets the string passed as label of that instance.

    """ 
    def __init__(self, label):
        """
        Constructor of class Place.

        Parameters
        ----------
        label : str
            any label passed by the user is set in this variable.

        Returns
        -------
        None.

        """       
        self.label = label
        self.transitions = []

class Transition:
    """
    This class is responsible for the change of state.

    Attributes
    ----------
    None.

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
            alphabet reflecting one activity of the instance from event log.
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

class Nfa:
    """
    This class makes the NFA model and validates by calculating fitness.

    Attributes
    ----------
    label : str
        sets direction of the code by showing what will be the next step now.
    places : list of str
        list of str to store activities from event log.
    transitions : list of str
        list of str responsible for change of state.
    start_place : str
        initial state of the NFA model. (Default: None)
    end_places : list of str
        list of str to store multiple ending states.
    Methods
    -------
    __init__ : constructor
       initialize the attributes and sets the label passed during instance creation.
    
    """ 
    def __init__(self, label):
        """
        initialize the attributes and sets the label passed during instance creation.

        Parameters
        ----------
        label : str
            sets direction of the code by showing what will be the next step now.
        places : list of str
            list of str to store activities from event log.
        transitions : list of str
            list of str responsible for change of state.
        start_place : str
            initial state of the NFA model. (Default: None)
        end_places : list of str
            list of str to store multiple ending states.

        Returns
        -------
        None.

        """      
        self.label = label
        self.places = []
        self.transitions = []
        self.start_place = None # here we use the definiton of an NFA with just one start place
        self.end_places = [] # but multiple acepting end places

    def print(self):
        print("Start place: " + self.start_place.label + str(self.places.index(self.start_place)))
        for place in self.places:
            print("Place: " + place.label + "_" + str(self.places.index(place)))
            if place in self.end_places:
                print("Endplace")
            for trans in place.transitions:
                print("" + trans.start_place.label + "_" + str(self.places.index(trans.start_place)) + " - " + trans.activity + " - " + trans.end_place.label + "_" + str(self.places.index(trans.end_place)))

    def add_place(self, place, is_start_place = False, is_end_place = False) :
        """
        sets labels. If start and end place values are not given in second and third argument, they are by default taken to be as False.

        Parameters
        ----------
        place : str
            alphabet reflecting label.
        is_start_Place : bool
            to check if its the start place. (Default: False)
        is_end_Place : bool
            to check if its the end place. (Default: False)

        Returns
        -------
        None.

        """ 
        #check whether place is a Place

        #check whether place allready exist
        self.places.append(place)
        if is_start_place :
            #check whether allready a start place is defined
            self.start_place = place
        if is_end_place :
            self.end_places.append(place)


    def remove_place(self, place) :
        """
        for removing an acitivity from the model.

        Parameters
        ----------
        place : str
            alphabet reflecting label. 

        Returns
        -------
        None.
        """ 
        #check whether place is a Place

        self.places.remove(place)

    def add_Transition(self, transition) :
        """
        adds an activity in the model alongwith its start and end place.

        Parameters
        ----------
        transition : list of str
            activity, its previous state and the next state.
        
        Returns
        -------
        None.

        """ 
        #check whether transition is a Transition
        #check whether transition only has places that exist
        #check for duplicate
        for place in self.places :
            if place == transition.start_place :
                place.transitions.append(transition)
                break

    def remove_Transition(self, transition) :
        """
        removes an activity from the model alongwith its start and end place.

        Parameters
        ----------
        transition : list of str
            activity, its previous state and the next state.
        
        Returns
        -------
        None.

        """ 
        #input checks
        for place in self.places :
            if place == transition.start_place :
                place.transitions.remove(transition)
                break

    def is_fitting(self, trace) :
      
        """
        checks if given trace mathces the model.

        Parameters
        ----------
        trace : list of str
            activities of an instance taken from event log.
        
        Returns
        -------
        bool
            true if it matches, false otherwise.

        """ 
        
        #trace is here just a list of activities
        #check input

        if(len(trace) == 0) :
            if self.start_place in self.end_places:
                return True
            #check only for epsilon transitions
            for trans in self.start_place.transitions :
                if trans.activity == SpecialActivities.EPSILON:
                    if( self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True) :
                        return True
            return False

        activity = trace[0]
        for trans in self.start_place.transitions :
            if trans.activity == activity :
                if( self.__is_subtrace_fitting(trans.end_place, trace[1:]) == True) :
                    return True
            if trans.activity == SpecialActivities.EPSILON:
                if( self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True) :
                    return True

        return False

    def __is_subtrace_fitting(self, current_place, trace) :

        """
        checks if given subtrace mathces the model.

        Parameters
        ----------
        trace : list of str
            activities of an instance taken from event log.
        
        Returns
        -------
        bool
            true if it matches, false otherwise.
        """ 
        #trace is here just a list of activities
        #check input

        if(len(trace) == 0) :
            if current_place in self.end_places:
                return True
            #check only for epsilon transitions
            for trans in current_place.transitions :
                if trans.activity == SpecialActivities.EPSILON:
                    if( self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True) :
                        return True
            return False

        activity = trace[0]
        for trans in current_place.transitions :
            if trans.activity == activity:
                if( self.__is_subtrace_fitting(trans.end_place, trace[1:]) == True) :
                    return True
            if trans.activity == SpecialActivities.EPSILON:
                if( self.__is_subtrace_fitting(trans.end_place, trace[0:]) == True) :
                    return True

        return False
    
    def log_fittness(self, log):
        """
        calculates fitness of the alignment.

        Parameters
        ----------
        log : list of str
            activities of an instance taken from event log.
        
        Returns
        -------
        bool
            needs to be discussed.
        """ 
        # Check for each trace in the log wether the trace is fiting (replayable)
        # return the fraction of traces that are fiting (replayable)
        return False # placeholder only

    def convert_from_regex(self, regex):
        #Check whether the nfa model is empty right now
        return False

# Expression := Konkat { "|" Konkat}
# Konkat := Prod {(".", "") Prod}      - until now the . is a must
# Prod := Factor ("*", "")
# Factor := Activity | "(" Expression ")"
#Activity := "a" | "b" | ... (all letters)

def expression(regex) :
    list_of_konkats = []
    list_of_konkats.append(konkat(regex))
    while(len(regex) > 0 and regex[0] == "|"):
        regex.pop(0)
        list_of_konkats.append(konkat(regex))
    return (unite_nfas(list_of_konkats))

def konkat(regex) :
    list_of_prods = []
    list_of_prods.append(prod(regex))
    while(len(regex) > 0 and regex[0] == "."):
        regex.pop(0)
        list_of_prods.append(prod(regex))
    return konkatonate_nfas(list_of_prods)

def prod(regex) :
    factor_nfa = factor(regex)
    if(len(regex) > 0 and regex[0] == "*"):
        regex.pop(0)
        return star_nfa(factor_nfa)
    return(factor_nfa)

def factor(regex) :
    if(len(regex) > 0 and regex[0].isalpha()):
        activity = regex.pop(0)
        activity_nfa = nfa_from_activity(activity)
        return activity_nfa
    if(len(regex) > 0 and regex[0] == "("):
        regex.pop(0)
        sub_nfa = expression(regex)
        if(len(regex) > 0 and regex[0] != "("):
            print("Error: Was expecting a closing parenthesis but recived: " + regex[0])
        regex.pop(0)
        return sub_nfa

#helping functions
def unite_nfas(nfas):

    if(len(nfas) == 1):
        return nfas[0]

    united_nfa = Nfa("unite")
    p_start = Place("u_s")
    united_nfa.add_place(p_start, True)
    p_end = Place("u_e")
    united_nfa.add_place(p_end, False, True)
    for nfa in nfas:
        #add places with their transitions
        for place in nfa.places:
            united_nfa.add_place(place)
        #connect the united start place to the start place of the nfa
        united_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, nfa.start_place))
        #connect all accepting places to the united accepting place
        for acc_place in nfa.end_places:
            united_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, p_end))
    return united_nfa

def konkatonate_nfas(nfas):

    if(len(nfas) == 1):
        return nfas[0]

    konkat_nfa = Nfa("konkat")
    p_start = Place("k_s")
    konkat_nfa.add_place(p_start, True)
    p_end = Place("k_e")
    konkat_nfa.add_place(p_end, False, True)
    for nfa in nfas:
        #add places with their transitions
        for place in nfa.places:
            konkat_nfa.add_place(place)
    #connect the accepting places of each nfa in the list to the start place of the following nfa  ---- optimisation potential by not going through the nfas twice
    for i in range(len(nfas)-1):
        for acc_plac in nfas[i].end_places:
            konkat_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_plac, nfas[i+1].start_place))

    #add Transition from new start to start of first nfa in list
    konkat_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, nfas[0].start_place))
    #add Transition from last nfa in list to new last place
    for acc_place in nfas[len(nfas)-1].end_places:
        konkat_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, p_end))
    
    return konkat_nfa

def star_nfa(nfa):
    star_nfa = Nfa("star")
    p_start = Place("s_s")
    star_nfa.add_place(p_start, True)
    p_end = Place("s_e")
    star_nfa.add_place(p_end, False, True)

    #add all places from nfa
    for place in nfa.places:
        star_nfa.add_place(place)

    #one can skip the nfa
    star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, p_end))
    #connect new start to the start of the nfa
    star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_start, nfa.start_place))
    #connect new end to the start of the nfa
    star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, p_end, nfa.start_place))

    #connect accepting places of the nfa to the new end place
    for acc_place in nfa.end_places:
        star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, p_end))

    return star_nfa


def nfa_from_activity(activity):
    base_nfa = Nfa("activity")
    p_start = Place("a_s")
    base_nfa.add_place(p_start, True)
    p_end = Place("a_e")
    base_nfa.add_place(p_end, False, True)
    base_nfa.add_Transition(Transition(activity, p_start, p_end))
    return base_nfa
    

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
print(myNFA.transitions)

print(myNFA.is_fitting(["a", "b", "c"])) #True
print(myNFA.is_fitting(["a", "b", "b", "b", "c"])) #True
print(myNFA.is_fitting(["a", "a", "b", "c"])) #False
print(myNFA.is_fitting(["a", "c"])) #False
print(myNFA.is_fitting(["a", "b"])) #False

myNFA.add_Transition(Transition(SpecialActivities.EPSILON, p2, p4))

print(myNFA.is_fitting(["a"])) #True

myRegexNfa = expression(["a", "*", "|", "(", "c", ".", "d", ")", "|", "(", "e", ".", "f", ")"])
myRegexNfa.print()

print("Regex: ")
print(myRegexNfa.is_fitting(["a", "a"])) #True
print(myRegexNfa.is_fitting(["a",])) #True
print(myRegexNfa.is_fitting([])) #True
print(myRegexNfa.is_fitting(["c", "d"])) #True
print(myRegexNfa.is_fitting(["e", "f"])) #True
print(myRegexNfa.is_fitting(["a", "c"])) #False
print(myRegexNfa.is_fitting(["a", "c", "d"])) #False
print(myRegexNfa.is_fitting(["x",])) #False
print(myRegexNfa.is_fitting(["c"])) #False