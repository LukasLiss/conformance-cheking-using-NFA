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
        self.start_place = None # here we use the definiton of an NFA with just one start place
        self.end_places = [] # but multiple acepting end places

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
                print("" + trans.start_place.label + "_" + str(self.places.index(trans.start_place)) + " - " + trans.activity + " - " + trans.end_place.label + "_" + str(self.places.index(trans.end_place)))

    def add_place(self, place, is_start_place = False, is_end_place = False) :
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
        This function removes a place from the NFA model.

        Parameters
        ----------
        place : Place object
            the place that needs to be removed from the NFA model. 

        Returns
        -------
        None.
        """ 
        #check whether place is a Place

        self.places.remove(place)

    def add_Transition(self, transition) :
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
        #check whether transition is a Transition
        #check whether transition only has places that exist
        #check for duplicate
        for place in self.places :
            if place == transition.start_place :
                place.transitions.append(transition)
                break

    def remove_Transition(self, transition) :
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
        #input checks
        for place in self.places :
            if place == transition.start_place :
                place.transitions.remove(transition)
                break

    def is_fitting(self, trace) :
      
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
        This function calculates fitness of the log (list of traces) when replayed on the NFA model.

        Parameters
        ----------
        log : list of list of strings
            instances/traces taken from event log.
        
        Returns
        -------
        variable: float
            the fitness value.
        """ 
        # Check for each trace in the log wether the trace is fiting (replayable)
        # return the fraction of traces that are fiting (replayable)
        return 1.0 # placeholder only

    def convert_from_regex(self, regex):
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

#Grammer used to describe the accepted regular expression:
# Expression := Konkat { "|" Konkat}
# Konkat := Prod {(".", "") Prod}  - until now the . is a must
# Prod := Factor ("*", "")
# Factor := Activity | "(" Expression ")"
# Activity := "a" | "b" | ... (all letters)

def expression(regex) :
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
    while(len(regex) > 0 and regex[0] == "|"):
        regex.pop(0)
        list_of_konkats.append(konkat(regex))
    return (unite_nfas(list_of_konkats))

def konkat(regex) :
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
    while(len(regex) > 0 and regex[0] == "."):
        regex.pop(0)
        list_of_prods.append(prod(regex))
    return konkatonate_nfas(list_of_prods)

def prod(regex) :
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
    if(len(regex) > 0 and regex[0] == "*"):
        regex.pop(0)
        return star_nfa(factor_nfa)
    return(factor_nfa)

def factor(regex) :
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