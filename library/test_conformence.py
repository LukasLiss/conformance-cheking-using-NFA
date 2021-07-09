from library.nfa import Nfa, Place, Transition, nfa_from_regex,SpecialActivities
from library import conformance
import unittest
class TestConformence(unittest.TestCase):
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
    def test_log_fittness(self):
        log1 = [["a", "b", "c"],["a", "b", "b", "b", "c"],["a", "a", "b", "c"],["a", "b", "c", "e"],["a", "c"],["a", "e"]]
        self.assertEqual(conformance.log_fittness(self.myNFA,log1),2/6)
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
        self.assertEqual(conformance.log_fittness(self.myNFA,log1), 3/6)
        self.assertEqual(conformance.log_fittness(self.myNFA,log2), 5/11)

    def test_is_trace_fitting(self):
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a", "b", "c"]))
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a", "b", "b", "b", "c"]))
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a", "a", "b", "c"]))
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a", "c"]))
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a", "b"]))
            p5 = Place("End")
            self.myNFA.add_place(p5, False, True)
            t5 = Transition("d", self.p3, p5)
            self.myNFA.add_Transition(t5)
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a"]))
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a", "b", "d"]))
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a", "b", "b", "b", "d"]))
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a", "a", "b", "d"]))
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a", "d"]))
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a", "e"]))
            p6 = Place("End")
            self.myNFA.add_place(p6, False, True)
            t6 = Transition("e", self.p2, p6)
            self.myNFA.add_Transition(t6)
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a", "e"]))
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a", "b","e"]))
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a", "b","b", "e"]))
            self.assertFalse(conformance.is_trace_fitting(self.myNFA,["a", "b", "c", "e"]))
            self.myNFA.add_Transition(Transition(SpecialActivities.EPSILON, self.p2, self.p4))
            self.assertTrue(conformance.is_trace_fitting(self.myNFA,["a"]))
    def test_optimal_alignment_trace_on_nfa(self):
        myTrace = ["a", "b", "b", "b", "c", "z"]
        self.assertEqual(conformance.optimal_alignment_trace_on_nfa(self.myNFA,myTrace),([('a', 'a'), ('b', 'b'), ('b', 'b'), ('b', 'b'), ('c', 'c'), ('z', '>>')], 1))
        myTrace = ["a", "z", "b", "b", "c"]
        self.assertEqual(conformance.optimal_alignment_trace_on_nfa(self.myNFA,myTrace),([('a', 'a'), ('z', '>>'), ('b', 'b'), ('b', 'b'), ('c', 'c')], 1))
        myTrace = ["a", "z", "b", "b"]
        self.assertEqual(conformance.optimal_alignment_trace_on_nfa(self.myNFA,myTrace),([('a', 'a'), ('z', '>>'), ('b', 'b'), ('b', 'b'), ('>>', 'c')], 2))
