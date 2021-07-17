import unittest
import conformance
import nfa
from nfa import Nfa, SpecialActivities
from nfa import Place
from nfa import Transition
class TestNfa(unittest.TestCase):
    def setUp(self) :
        self.myNFA = Nfa("TestNFA")
        self.p1 = Place("Greating")
        self.myNFA.add_place(self.p1, True)
        self.p2 = Place("Start Small Talk")
        self.myNFA.add_place(self.p2)
        self.p3 = Place("End Small Talk")
        self.myNFA.add_place(self.p3)
        self.p4 = Place("Good Bye")
        self.myNFA.add_place(self.p4, False, True)
        self.t1 = Transition("a", self.p1, self.p2)
        self.myNFA.add_Transition(self.t1)
        self.t2 = Transition("b", self.p2, self.p2)
        self.myNFA.add_Transition(self.t2)
        self.t3 = Transition("b", self.p2, self.p3)
        self.myNFA.add_Transition(self.t3)
        self.t4 = Transition("c", self.p3, self.p4)
        self.myNFA.add_Transition(self.t4)

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    @classmethod
    def tearDownClass(cls):
        pass
    def test_add_Place(self):
        p5 = Place("Go")
        self.myNFA.add_place(p5, False, True)
        length = len(self.myNFA.places)
        self.assertEqual(length, 5)
        self.assertEqual(self.myNFA.places, [self.p1, self.p2, self.p3, self.p4, p5])
        self.assertEqual(self.myNFA.start_place, self.p1)
        p6 = Place("Go")
        self.myNFA.add_place(p6, True, True)
        self.assertEqual(self.myNFA.places, [self.p1, self.p2, self.p3, self.p4, p5,p6])
        self.assertEqual(self.myNFA.start_place, self.p1)
        self.assertEqual(self.myNFA.end_places,[self.p4,p5, p6])

    def test_remove_place(self):
        self.myNFA.remove_place(self.p4)
        self.assertEqual(self.myNFA.places,[self.p1,self.p2,self.p3])
        p5 = Place("Go")
        self.myNFA.add_place(p5, False, True)
        self.assertEqual(self.myNFA.places, [self.p1, self.p2, self.p3,p5])

    def test_add_transition(self):
        self.assertEqual(self.p2.transitions, [self.t2, self.t3])
        p5 = Place("Go")
        self.myNFA.add_place(p5, False, True)
        t5 = Transition("c", self.p4, p5)
        self.myNFA.add_Transition(t5)
        self.assertEqual(self.p4.transitions, [t5])

    def test_remove_Transition(self):
        self.myNFA.remove_Transition(self.t2)
        self.assertEqual(self.p2.transitions, [self.t3])
        p5 = Place("Go")
        self.myNFA.add_place(p5, False, True)
        t5 = Transition("c", self.p4, p5)
        self.myNFA.add_Transition(t5)
        self.assertEqual(self.p4.transitions, [t5])
        self.myNFA.remove_Transition(t5)
        self.assertEqual(self.p4.transitions, [])

    def test_re_expression_check(self):
        test_regexs = [["a", "b", "b", "b", "c"],["a", "*", "b", ".", "c"],["a", ".", "b", "|", "c"],
                       ["(", "A", "-", "Z", "a", "-", "z","0","-","9",")"],["a","b","\\"],
                       ["(","a","b","c","("],["["],["[", ".", "*"]]
        for i in range(3):
            self.assertTrue(nfa.re_expression_check(test_regexs[i]))
        for i in range(3,8):
            self.assertFalse(nfa.re_expression_check(test_regexs[i]))

    def test_expression(self):
        myRegexNfa = nfa.expression(["a", "*", "|", "(", "c", ".", "d", ")", "|", "(", "e", ".", "f", ")"])
        test_Traces = [["a", "a","a"],["a"],[],["c", "d"],["e", "f"],["a", "c"],["a", "c", "d"],["x"],["c"]]
        for i in range(5):
            self.assertTrue(conformance.is_trace_fitting(myRegexNfa, test_Traces[i]))
        for i in range(5, 9):
            self.assertFalse(conformance.is_trace_fitting(myRegexNfa, test_Traces[i]))

    def test_nfa_from_regex(self):
        regex = (["a", "*", "|", "(", "b", ".", "c", ")", "|", "(", "d", ".", "e", ")"])
        test_Traces = [["a", "b"],["a","b","b","b","b","b","c","z'"],["a", "b", "c", "d", "e"],["a","a","a"],[],["b","c"],
                       ["d","e"]]
        myNfa = nfa.nfa_from_regex(regex)
        for i in range(3):
            self.assertFalse(conformance.is_trace_fitting(myNfa, test_Traces[i]))
        for i in range(3,7):
            self.assertTrue(conformance.is_trace_fitting(myNfa, test_Traces[i]))


    def test_trace_check(self):
        myTrace = ["a", "b", "b", "b", "c", "z"]
        self.assertTrue(nfa.trace_check(myTrace))
        myTrace = ["a", "*", "b", "/", "c", "z"]
        self.assertFalse(nfa.trace_check(myTrace))
        myTrace = ["a", "b", "b", "b", "b", "b", "cc", "z'"]
        self.assertFalse(nfa.trace_check(myTrace))
        myTrace = ["a", "b", "b", "0", "b", "1", "c", "z"]
        self.assertTrue(nfa.trace_check(myTrace))
    def test_nfa_from_activity(self):
        myNfa = nfa.nfa_from_activity("a")
        trace = ["a"]
        self.assertTrue(conformance.is_trace_fitting(myNfa, trace))
    def test_factor(self):
        myNfa = nfa.factor(["c"])
        trace1 = ["c"]
        trace2 = ["a"]
        self.assertTrue(conformance.is_trace_fitting(myNfa, trace1))
        self.assertFalse(conformance.is_trace_fitting(myNfa, trace2))
        myNfa = nfa.factor(["(", "b", ".", "c", ")"])
        trace1 = ["b","c"]
        trace2 = ["a","b"]
        self.assertTrue(conformance.is_trace_fitting(myNfa, trace1))
        self.assertFalse(conformance.is_trace_fitting(myNfa, trace2))
    def test_prod(self):
        regex = (["a", "*", "|", "(", "b", ".", "c", ")", "|", "(", "d", ".", "e", ")"])
        myNfa = nfa.prod(regex)
        test_Traces = [["a"], ["a", "a"],["a","a","a"],["b","c"]]
        for i in range(3):
            self.assertTrue(conformance.is_trace_fitting(myNfa, test_Traces[i]))
        for i in range(3, 4):
            self.assertFalse(conformance.is_trace_fitting(myNfa, test_Traces[i]))
    def test_konkat(self):
        myNFA = nfa.konkat(["(", "e", ".", "f", ")"])
        test_Traces = [["e", "f"], ["a", "a", "a"], ["b", "c"],["e"],["f"]]
        for i in range(1):
            self.assertTrue(conformance.is_trace_fitting(myNFA, test_Traces[i]))
        for i in range(1, 4):
            self.assertFalse(conformance.is_trace_fitting(myNFA, test_Traces[i]))

    def test_star_nfa(self):
        test_Traces = [["a","b","c"],["a","b","c","a","b","c"],["a","b","b","b","c","a","b","c"],
                       ["a", "b", "b", "b", "c", "a", "b","b", "c","a","b","c"],[],["a","b","c","a","c"],["a", "b"]]
        star_NFA = nfa.star_nfa(self.myNFA)
        for i in range(5):
            self.assertTrue(conformance.is_trace_fitting(star_NFA, test_Traces[i]))
        for i in range(5, 7):
            self.assertFalse(conformance.is_trace_fitting(star_NFA, test_Traces[i]))
    def test_konkatonate_nfas(self):
        firstNFA = nfa.expression(["(", "e", ".", "f", ")"])
        secondNFA = self.myNFA
        concatNFA = nfa.konkatonate_nfas([secondNFA,firstNFA])
        test_Traces = [["a", "b", "c","e","f"],["a", "b", "b", "b", "c","e","f"],["a", "b", "b", "c","e","f"],[],
                       ["e","f"],["a", "b", "c", "e"],["a", "b","c"]]
        for i in range(3):
            self.assertTrue(conformance.is_trace_fitting(concatNFA, test_Traces[i]))
        for i in range(3, 7):
            self.assertFalse(conformance.is_trace_fitting(concatNFA, test_Traces[i]))

    def test_unite_nfas(self):
        firstNFA = nfa.expression(["d", "*", "|","(", "e", ".", "f", ")"])
        secondNFA = self.myNFA
        unionNFA = nfa.unite_nfas([secondNFA, firstNFA])
        test_Traces = [["a", "b", "c"],["a", "b", "b", "b", "c"],["a", "b", "b", "c"],["d","d","d"],
                  ["e", "f"],["d"],[],["a", "b", "c","d","d","d"],["a", "b", "c", "e", "f"],
                  ["a", "b","b","c", "d"]]
        for i in range(7):
            self.assertTrue(conformance.is_trace_fitting(unionNFA, test_Traces[i]))
        for i in range(8, 10):
            self.assertFalse(conformance.is_trace_fitting(unionNFA, test_Traces[i]))









