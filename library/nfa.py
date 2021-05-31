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
    def __init__(self, activity, start_Place, end_Place):
        """
        Constructor of class Transition that sets values of the instance.

        Parameters
        ----------
        activity : str
            alphabet reflecting one activity of the instance from event log.
        start_Place : str
            start state of the activity at hand.
        end_Place : str
            end state of the activity at hand.

        Returns
        -------
        None.

        """         
        self.activity = activity
        self.start_Place = start_Place
        self.end_Place = end_Place

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

    def add_Place(self, place, is_start_place = False, is_end_place = False) :
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

    def remove_Place(self, place) :
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
        self.transitions.append(transition)

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
        self.transitions.remove(transition)

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
        #print("Fit with: " + self.start_place.label + " " + ''.join(trace))
        #trace is here just a list of activities
        #check input

        if(len(trace) == 0) :
            return (self.start_place in self.end_places)

        activity = trace[0]
        for trans in self.transitions : # performance increase possible by having a reference to connected transition of each place, but increases memory usage
            if((trans.start_Place == self.start_place) and (trans.activity == activity)) :
                if( self.__is_subtrace_fitting(trans.end_Place, trace[1:]) == True) :
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
        #print("Sub with: " + current_place.label + " " + ''.join(trace))
        #trace is here just a list of activities
        #check input

        if(len(trace) == 0) :
            return (current_place in self.end_places)

        activity = trace[0]
        for trans in self.transitions : # performance increase possible by having a reference to connected transition of each place, but increases memory usage
            if((trans.start_Place == current_place) and (trans.activity == activity)) :
                if( self.__is_subtrace_fitting(trans.end_Place, trace[1:]) == True) :
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
        return False # Placeholder only


# Test section

myNFA = Nfa("TestNFA")
p1 = Place("Greating")
myNFA.add_Place(p1, True)
p2 = Place("Start Small Talk")
myNFA.add_Place(p2)
p3 = Place("End Small Talk")
myNFA.add_Place(p3)
p4 = Place("Good Bye")
myNFA.add_Place(p4, False, True)
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