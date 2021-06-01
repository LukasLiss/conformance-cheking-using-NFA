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
    united_nfa = Nfa("unite")
    p_start = Place("u_start")
    united_nfa.add_place(p_start, True)
    p_end = Place("u_end")
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
    konkat_nfa = Nfa("unite")
    p_start = Place("u_start")
    konkat_nfa.add_place(p_start, True)
    p_end = Place("u_end")
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
    return False

def nfa_from_activity(activity):
    base_nfa = Nfa("unite")
    p_start = Place("u_start")
    base_nfa.add_place(p_start, True)
    p_end = Place("u_end")
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

# print(myNFA.is_fitting(["a", "b", "c"])) #True
# print(myNFA.is_fitting(["a", "b", "b", "b", "c"])) #True
# print(myNFA.is_fitting(["a", "a", "b", "c"])) #False
# print(myNFA.is_fitting(["a", "c"])) #False
# print(myNFA.is_fitting(["a", "b"])) #False

myNFA.add_Transition(Transition(SpecialActivities.EPSILON, p2, p4))

print(myNFA.is_fitting(["a"])) #True

myRegexNfa = expression(["a", "b", "c"])
print("Regex: ")
print(myRegexNfa.is_fitting(["a", "b", "c"])) #True