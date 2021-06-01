class SpecialActivities:
    EPSILON = '\u03B5'

class Place:
    def __init__(self, label):
        self.label = label
        self.transitions = []

class Transition:
    def __init__(self, activity, start_place, end_place):
        self.activity = activity
        self.start_place = start_place
        self.end_place = end_place

class Nfa:
    def __init__(self, label):
        self.label = label
        self.places = []
        self.transitions = []
        self.start_place = None # here we use the definiton of an NFA with just one start place
        self.end_places = [] # but multiple acepting end places

    def add_place(self, place, is_start_place = False, is_end_place = False) :
        #check whether place is a place
        #check whether place allready exist
        self.places.append(place)
        if is_start_place :
            #check whether allready a start place is defined
            self.start_place = place
        if is_end_place :
            self.end_places.append(place)

    def remove_place(self, place) :
        #check whether place is a place
        self.places.remove(place)

    def add_Transition(self, transition) :
        #check whether transition is a Transition
        #check whether transition only has places that exist
        #check for duplicate
        for place in self.places :
            if place == transition.start_place :
                place.transitions.append(transition)
                break

    def remove_Transition(self, transition) :
        #input checks
        for place in self.places :
            if place == transition.start_place :
                place.transitions.remove(transition)
                break

    def is_fitting(self, trace) :
        #trace is here just a list of activities
        #check input

        if(len(trace) == 0) :
            return (self.start_place in self.end_places)

        activity = trace[0]
        for trans in self.start_place.transitions :
            if ((trans.activity == activity) or ((trans.activity == SpecialActivities.EPSILON))) :
                if( self.__is_subtrace_fitting(trans.end_place, trace[1:]) == True) :
                    return True

        return False

    def __is_subtrace_fitting(self, current_place, trace) :
        #trace is here just a list of activities
        #check input

        if(len(trace) == 0) :
            return (current_place in self.end_places)

        activity = trace[0]
        for trans in current_place.transitions : # performance increase possible by having a reference to connected transition of each place, but increases memory usage
            if ((trans.activity == activity) or (trans.activity == SpecialActivities.EPSILON)) :
                if( self.__is_subtrace_fitting(trans.end_place, trace[1:]) == True) :
                    return True

        return False
    
    def log_fittness(self, log):
        # Check for each trace in the log wether the trace is fiting (replayable)
        # return the fraction of traces that are fiting (replayable)
        return False # placeholder only

    def convert_from_regex(self, regex):
        #Check whether the nfa model is empty right now
        return False


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