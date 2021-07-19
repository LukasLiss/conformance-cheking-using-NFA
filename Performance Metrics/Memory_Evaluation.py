from library import conformance, nfa
from memory_profiler import memory_usage
regex = ["(", "a", ".", "b", "*", ".", "c", ".", "d", "*", ".", "e", ".", "f", "*", ".", "g", "|", "a",".", "b", "*",".", "i",".", "j",
     "*",".", "k",".", "l", "*","." ,"m",".", "g", ")"]
myNfa = nfa.nfa_from_regex(regex)

def conformrnce_small():
    test_Traces = []
    file = open("small_DataSet.txt", "r")
    for number,str in  enumerate(file):
        #the other approach
        #conformance.optimal_alignment_trace_on_nfa(myNfa, list(str.rstrip()))
        test_Traces.append(list(str.rstrip()))
    for number,trace in enumerate(test_Traces):
        print(number)
        print(conformance.optimal_alignment_trace_on_nfa(myNfa,test_Traces[number]))
    file.close()
    return
def conformrnce_medium():
    test_Traces = []
    file = open("medium_DataSet.txt", "r")
    for str in file:
        # the other approach
        # conformance.optimal_alignment_trace_on_nfa(myNfa, list(str.rstrip()))
        test_Traces.append(list(str.rstrip()))
    print(len(test_Traces))
    for number,trace in enumerate(test_Traces):
        print(number)
        conformance.optimal_alignment_trace_on_nfa(myNfa,test_Traces[number])
    file.close()
    return
def conformrnce_large():
    test_Traces = []
    file = open("larg_DataSet.txt", "r")
    for str in file:
        # the other approach
        # conformance.optimal_alignment_trace_on_nfa(myNfa, list(str.rstrip()))
        test_Traces.append(list(str.rstrip()))
    for number,trace in enumerate(test_Traces):
        print(number)
        print(conformance.optimal_alignment_trace_on_nfa(myNfa,test_Traces[number]))
    file.close()
    return


if __name__ == '__main__':
      f_log = open("Evaluation_log.txt", "a+")
      max_memory_small_file = max(memory_usage(conformrnce_small))
     # max_memory_medium_file = max(memory_usage(conformrnce_medium))
     # # max_memory_large_file = max(memory_usage(conformrnce_large))
      f_log.write("memory_small "+ str(round(max_memory_small_file,2)) + '\n')
     # f_log.write("memory_medium " + str(round(max_memory_medium_file, 2)) + '\n')
     # # f_log.write("memory_large "+str(round(max_memory_large_file, 2)) + '\n')
