import unittest
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
    def test_is_fitting(self):
            self.assertTrue(self.myNFA.is_fitting(["a", "b", "c"]))
            self.assertTrue(self.myNFA.is_fitting(["a", "b", "b", "b", "c"]))
            self.assertFalse(self.myNFA.is_fitting(["a", "a", "b", "c"]))
            self.assertFalse(self.myNFA.is_fitting(["a", "c"]))
            self.assertFalse(self.myNFA.is_fitting(["a", "b"]))
            p5 = Place("End")
            self.myNFA.add_place(p5, False, True)
            t5 = Transition("d", self.p3, p5)
            self.myNFA.add_Transition(t5)
            self.assertFalse(self.myNFA.is_fitting(["a"]))
            self.assertTrue(self.myNFA.is_fitting(["a", "b", "d"]))
            self.assertTrue(self.myNFA.is_fitting(["a", "b", "b", "b", "d"]))
            self.assertFalse(self.myNFA.is_fitting(["a", "a", "b", "d"]))
            self.assertFalse(self.myNFA.is_fitting(["a", "d"]))
            self.assertFalse(self.myNFA.is_fitting(["a", "e"]))
            p6 = Place("End")
            self.myNFA.add_place(p6, False, True)
            t6 = Transition("e", self.p2, p6)
            self.myNFA.add_Transition(t6)
            self.assertTrue(self.myNFA.is_fitting(["a", "e"]))
            self.assertTrue(self.myNFA.is_fitting(["a", "b","e"]))
            self.assertTrue(self.myNFA.is_fitting(["a", "b","b", "e"]))
            self.assertFalse(self.myNFA.is_fitting(["a", "b", "c", "e"]))
            self.myNFA.add_Transition(Transition(SpecialActivities.EPSILON, self.p2, self.p4))
            self.assertTrue(self.myNFA.is_fitting(["a"]))

    def test_log_fittness(self):
        log1 = [["a", "b", "c"],["a", "b", "b", "b", "c"],["a", "a", "b", "c"],["a", "b", "c", "e"],["a", "c"],["a", "e"]]
        self.assertEqual(self.myNFA.log_fittness(log1),2/6)
        log2 =[["a", "b", "c"],["a", "b", "b", "b", "c"],["a", "a", "b", "c"],["a", "b", "c", "e"],["a", "c"],["a", "e"],["a", "d"],["a"],["a", "b","e"],["a", "b", "c", "e"],["a","c","d","e"]]
        p5 = Place("End")
        self.myNFA.add_place(p5, False, True)
        t5 = Transition("d", self.p3, p5)
        self.myNFA.add_Transition(t5)
        p6 = Place("End")
        self.myNFA.add_place(p6, False, True)
        t6 = Transition("e", self.p2, p6)
        self.myNFA.add_Transition(t6)
        self.myNFA.add_Transition(Transition(SpecialActivities.EPSILON, self.p2, self.p4))
        self.assertEqual(self.myNFA.log_fittness(log1), 3/6)
        self.assertEqual(self.myNFA.log_fittness(log2), 5/11)

    def test_re_expression_check(self):
        self.assertTrue(nfa.re_expression_check(["a", "b", "b", "b", "c"]))
        self.assertFalse(nfa.re_expression_check(["a","b","\\"]))
        self.assertTrue(nfa.re_expression_check(["a", "*", "b", "+", "c"]))
        self.assertFalse(nfa.re_expression_check(["["]))
        self.assertFalse(nfa.re_expression_check(["(","a","b","c","("]))
        self.assertTrue(nfa.re_expression_check(["a", "*", "b", "+", "c"]))
        self.assertFalse(nfa.re_expression_check(["[","0", "-", "9", "]","+","+"]))
        self.assertTrue(nfa.re_expression_check(["a", "*", "b", "+", "c"]))
        self.assertFalse(nfa.re_expression_check(["[", ".", "*"]))
        self.assertTrue(nfa.re_expression_check(["(", "A", "-", "Z", "a", "-", "z","0","-","9",")"]))

    def test_expression(self):
        myRegexNfa = nfa.expression(["a", "*", "|", "(", "c", ".", "d", ")", "|", "(", "e", ".", "f", ")"])
        self.assertTrue(myRegexNfa.is_fitting(["a", "a","a"]))
        self.assertTrue(myRegexNfa.is_fitting(["a"]))
        self.assertTrue(myRegexNfa.is_fitting([]))
        self.assertTrue(myRegexNfa.is_fitting(["c", "d"]))
        self.assertTrue(myRegexNfa.is_fitting(["e", "f"]))
        self.assertFalse(myRegexNfa.is_fitting(["a", "c"]))
        self.assertFalse(myRegexNfa.is_fitting(["a", "c", "d"]))
        self.assertFalse(myRegexNfa.is_fitting(["x"]))
        self.assertFalse(myRegexNfa.is_fitting(["c"]))

    def test_nfa_from_trace(self):
        myTrace = ["a", "b", "b", "b", "c", "z"]
        trace1 = ["a", "b"]
        trace2 = ["a","b","b","b","b","b","c","z'"]
        myNfa = nfa.nfa_from_trace(myTrace)
        self.assertTrue(myNfa.is_fitting(myTrace))
        self.assertFalse(myNfa.is_fitting(trace1))
        self.assertFalse(myNfa.is_fitting(trace2))
    def test_align_trace(self):
        myTrace = ["a", "b", "b", "b", "c", "z"]
        self.assertEqual(self.myNFA.align_trace(myTrace),([('a', 'a'), ('b', 'b'), ('b', 'b'), ('b', 'b'), ('c', 'c'), ('z', '>>')], 1))
        myTrace = ["a", "z", "b", "b", "c"]
        self.assertEqual(self.myNFA.align_trace(myTrace),([('a', 'a'), ('z', '>>'), ('b', 'b'), ('b', 'b'), ('c', 'c')], 1))
        myTrace = ["a", "z", "b", "b"]
        self.assertEqual(self.myNFA.align_trace(myTrace),([('a', 'a'), ('z', '>>'), ('b', 'b'), ('b', 'b'), ('>>', 'c')], 2))