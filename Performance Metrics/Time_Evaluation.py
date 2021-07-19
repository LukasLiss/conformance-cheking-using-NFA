import timeit
import time
from library import conformance, nfa
regex = ["(", "a", ".", "b", "*", ".", "c", ".", "d", "*", ".", "e", ".", "f", "*", ".", "g", "|", "a",".", "b", "*",".", "i",".", "j",
     "*",".", "k",".", "l", "*","." ,"m",".", "g", ")"]
myNfa = nfa.nfa_from_regex(regex)
def log_elements():
    test_Traces = []
    file = open("elements.txt", "r")
    f_log = open("elements_log.txt", "a+")
    for number,strng in  enumerate(file):
        #the other approach
        #conformance.optimal_alignment_trace_on_nfa(myNfa, list(strng.rstrip()))
        test_Traces.append(list(strng.rstrip()))
    for number,trace in enumerate(test_Traces):
        start = time.time()
        print(conformance.optimal_alignment_trace_on_nfa(myNfa,test_Traces[number]))
        time.sleep(0.1)
        end = time.time()
        f_log.write(str(round(end - start,2)) + '\n')
    file.close()
    f_log.close()
    return

setup_code = "from library import conformance,nfa"

small_statement = """
regex = ["(", "a", ".", "b", "*", ".", "c", ".", "d", "*", ".", "e", ".", "f", "*", ".", "g", "|", "a",".", "b", "*",".", "i",".", "j",
     "*",".", "k",".", "l", "*","." ,"m",".", "g", ")"]
myNfa = nfa.nfa_from_regex(regex)
test_Traces = []
file = open("small_DataSet.txt", "r")
for number,str in  enumerate(file):
    #the other approach
    #conformance.optimal_alignment_trace_on_nfa(myNfa, list(str.rstrip()))
    test_Traces.append(list(str.rstrip()))
for number,trace in enumerate(test_Traces):
    print(len(test_Traces))
    print(number)
    print(conformance.optimal_alignment_trace_on_nfa(myNfa,trace))
file.close()
    """
medium_statement = """
regex = ["(", "a", ".", "b", "*", ".", "c", ".", "d", "*", ".", "e", ".", "f", "*", ".", "g", "|", "a",".", "b", "*",".", "i",".", "j",
     "*",".", "k",".", "l", "*","." ,"m",".", "g", ")"]
myNfa = nfa.nfa_from_regex(regex)
test_Traces = []
file = open("medium_DataSet.txt", "r")
for number,str in  enumerate(file):
    #the other approach
    #conformance.optimal_alignment_trace_on_nfa(myNfa, list(str.rstrip()))
    test_Traces.append(list(str.rstrip()))
print(len(test_Traces))
for number,trace in enumerate(test_Traces):
    print(number)
    conformance.optimal_alignment_trace_on_nfa(myNfa,trace)
file.close()
    """
large_statement = """
regex = ["(", "a", ".", "b", "*", ".", "c", ".", "d", "*", ".", "e", ".", "f", "*", ".", "g", "|", "a",".", "b", "*",".", "i",".", "j",
     "*",".", "k",".", "l", "*","." ,"m",".", "g", ")"]
myNfa = nfa.nfa_from_regex(regex)
test_Traces = []
file = open("large_DataSet.txt", "r")
for number,str in  enumerate(file):
    #the other approach
    #conformance.optimal_alignment_trace_on_nfa(myNfa, list(str.rstrip()))
    test_Traces.append(list(str.rstrip()))
print(len(test_Traces))
for number,trace in enumerate(test_Traces):
    print(number)
    conformance.optimal_alignment_trace_on_nfa(myNfa,trace)
file.close()
    """
f_log = open("Evaluation_log.txt", "a+")
small_time = timeit.timeit(setup = setup_code, stmt= small_statement,number=1)
# #medium_time = timeit.timeit(setup = setup_code, stmt= medium_statement,number=1)
#
# large_time = timeit.timeit(setup = setup_code, stmt= large_statement,number=1)
# print(medium_time)
f_log.write("time_small "+ str(round(small_time,2)) + '\n')
# #f_log.write("time_medium " + str(round(medium_time, 2)) + '\n')
# f_log.write("memory_large "+large_time + '\n')
log_elements()
