class Place:
    def __init__(self, label):
        self.label = label

class Transition:
    def __init__(self, activity, start_Place, end_Place):
        self.activity = activity
        self.start_Place = start_Place
        self.end_Place = end_Place

class Nfa:
    def __init__(self, label):
        self.label = label
        self.places = []
        self.transitions = []
        self.start_place = None # here we use the definiton of an NFA with just one start place
        self.end_places = [] # but multiple acepting end places

    def add_Place(self, place, is_start_place = False, is_end_place = False) :
        #check whether place is a Place
        #check whether place allready exist
        self.places.append(place)
        if is_start_place :
            #check whether allready a start place is defined
            self.start_place = place
        if is_end_place :
            self.end_places.append(place)

    def remove_Place(self, place) :
        #check whether place is a Place
        self.places.remove(place)

    def add_Transition(self, transition) :
        #check whether transition is a Transition
        #check whether transition only has places that exist
        #check for duplicate
        self.transitions.append(transition)

    def remove_Transition(self, transition) :
        #input checks
        self.transitions.remove(transition)

    def is_fitting(self, trace) :
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