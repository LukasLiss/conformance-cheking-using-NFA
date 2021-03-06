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


def nfa_from_regex(regex):
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
    input_regex_check_flag = re_expression_check(regex)
    if not input_regex_check_flag:
        exit()
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
    if (len(regex) > 0 and regex[0].isalpha()):
        activity = regex.pop(0)
        activity_nfa = nfa_from_activity(activity)
        return activity_nfa
    if (len(regex) > 0 and regex[0] == "("):
        regex.pop(0)
        sub_nfa = expression(regex)
        if (len(regex) > 0 and regex[0] != ")"):
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

    # connect accepting places of the nfa to the new end place
    for acc_place in nfa.end_places:
        star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, p_end))
        star_nfa.add_Transition(Transition(SpecialActivities.EPSILON, acc_place, nfa.start_place))

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


def trace_check(trace):  # done
    """
    Fucntion that checks whether the given trace is valid or not.

    Parameters
    ----------
    trace : list of strings
        instance taken from event log.

    Returns
    -------
    bool
        true if the given trace fulfills criteria for trace and false in case it does not.
    """
    if not isinstance(trace, list):
        print("Input is not a list")
        return False
    for i in trace:
        i = i.replace(" ", "")
        if not i.isalnum():
            print("Only alphanumeric values are allowed")
            return False

    return True


def re_expression_check(reg):  # done
    """
    Fucntion that checks whether the input is a regular expression.

    Parameters
    ----------
    reg : list of characters
        regular expressions that will be validated.

    Returns
    -------
    bool
        true if given list of strings fulfills crtieria of reg expression and false if it does not.
    """
    special_characters = ["*", "|", ".", "(", ")"]
    count1 = 0

    if not isinstance(reg, list):
        print("Input is not a list")
        return False
    for i in reg:
        if (i.isalnum() or i in special_characters) and not len(i) == 1:
            print("Only single characters are allowed")
            return False

        if not i.isalnum() and i not in special_characters:
            print("Only alphanumeric values with given set of special characters [| * . ( ) ] are allowed")
            return False
        if i == "(":
            count1 += 1
        if i == ")":
            count1 -= 1
        if count1 < 0:
            print("Invalid Expression: Missing opening bracket")
            return False
    if count1 != 0:
        print("Invalid Expression: Closing bracket not found")
        return False
    return True


def log_check(log):
    for value in log:
       check = trace_check(value)
       if not check:
           exit()


    return True
