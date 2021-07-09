from library.nfa import Nfa, Place, Transition, nfa_from_regex
from library import conformance, nfa
myNFA = Nfa("Small Talk Nfa")
p1 = Place("Greating")
myNFA.add_place(p1, True)
p2 = Place("Start Small Talk")
myNFA.add_place(p2)
p3 = Place("End Small Talk")
myNFA.add_place(p3)
p4 = Place("Good Bye")
myNFA.add_place(p4, False, True)
t1 = Transition("hello", p1, p2)
myNFA.add_Transition(t1)
t2 = Transition("small talk", p2, p2)
myNFA.add_Transition(t2)
t3 = Transition("small talk", p2, p3)
myNFA.add_Transition(t3)
t4 = Transition("good by", p3, p4)
myNFA.add_Transition(t4)

# The small talk nfa requires a "hello" then at least one "small talk" and one "good by" in the end
print("\nCheck wether traces are perfectly fitting with the Small Talk Nfa: \n")
current_Trace = ["hello", "small talk", "good by"]
print("Trace: ", current_Trace, " is fitting: ", conformance.is_trace_fitting(myNFA, current_Trace))  # True
current_Trace = ["hello", "small talk", "small talk", "small talk", "good by"]
print("Trace: ", current_Trace, " is fitting: ", conformance.is_trace_fitting(myNFA, current_Trace))  # True
current_Trace = ["hello", "hello", "small talk", "good by"]
print("Trace: ", current_Trace, " is fitting: ", conformance.is_trace_fitting(myNFA, current_Trace))  # False
current_Trace = ["hello", "good by"]
print("Trace: ", current_Trace, " is fitting: ", conformance.is_trace_fitting(myNFA, current_Trace))  # False
current_Trace = ["hello", "small talk"]
print("Trace: ", current_Trace, " is fitting: ", conformance.is_trace_fitting(myNFA, current_Trace))  # False

print("\nCompute Alignments for those traces that are not matching: \n")
current_Trace = ["hello", "hello", "small talk", "good by"]
print(conformance.optimal_alignment_trace_on_nfa(myNFA, current_Trace))
current_Trace = ["hello", "good by"]
print(conformance.optimal_alignment_trace_on_nfa(myNFA, current_Trace))
current_Trace = ["hello", "small talk"]
print(conformance.optimal_alignment_trace_on_nfa(myNFA, current_Trace))

print("\nA trace that has more deviations has higher cost of the alignment:\n")
current_Trace = ["hello", "hello", "politics", "politics", "good by"]
print(conformance.optimal_alignment_trace_on_nfa(myNFA, current_Trace))

print("\nOne can create an Nfa easily from a regular expression:\n")
myRegexNfa = nfa_from_regex(["a", "*", "|", "(", "c", ".", "d", ")", "|", "(", "e", ".", "f", ")"])
print("Here we used: ", ["a", "*", "|", "(", "c", ".", "d", ")", "|", "(", "e", ".", "f", ")"], " as the regular expression. The nfa is intended to accept arbitrary many a, or c followed by d, or e followed by f")
print("By computing alignments for some traces we can see that this work correctly:\n")
current_Trace = ["a", "a"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))
current_Trace = ["a", "a", "a", "a"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))
current_Trace = ["c", "d"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))
current_Trace = ["e", "f"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))
current_Trace = ["a", "c"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))
current_Trace = ["c", "d", "c", "d"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))
current_Trace = ["c", "f"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))

print("\nLets use a more complex regular expression:\n")
myRegexNfa = nfa_from_regex(["a", ".", "(", "b", "*", ")", ".", "(", "(", "c", ".", "d", ")", "*", ")" ])
current_Trace = ["a", "x", "b", "b", "y", "c", "d", "c", "d", "c"]
print(conformance.optimal_alignment_trace_on_nfa(myRegexNfa, current_Trace))

print("\nThese operations work also on logs instead of traces: \n")
example_log = [["a"], ["a", "b"], ["a", "b", "b"], ["a", "c", "d"], ["x"], ["x", "y"], ["y"], ["w"], ["k"], ["q"]]
print("\nThe percentage of fiting traces of an example log L is: ", conformance.log_fittness(myRegexNfa, example_log)) #0.4 is correct (first 4 of the 10 traces match)

print("\nAn alignment for a different log can look like the following:\n")
example_log_2 = [["a"], ["a", "c", "d"], ["b"], ["a", "c"]]
print(conformance.optimal_alignment_log_on_nfa(myRegexNfa, example_log_2))