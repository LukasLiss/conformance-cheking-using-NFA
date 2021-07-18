import os
import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import statistics
import numpy as np
import pm4py
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.discovery.parameters import Parameters
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from library import conformance, nfa
from memory_profiler import memory_usage

regex = ["a", ".", "(", "(", "(", "b", ".", "c", "|", "c", ".", "b", "|", "b", ".", "d", "|", "d", ".", "b", ")", ".",
         "e", ")", "|", "f", ")", "*", ".", "(", "g", "|", "h", ")"]
myNfa = nfa.nfa_from_regex(regex)


def memory_eval_petri():
    log = xes_importer.apply(os.path.join("running-example.xes"))
    net, initial_marking, final_marking = inductive_miner.apply(log)
    # if you want to view the petri net generated
    # viz_pn = pn_vis_factory.apply(net, initial_marking, final_marking)
    # pn_vis_factory.view(viz_pn)
    # viz = pm4py.visualization.petrinet.common.visualize.graphviz_visualization(net, image_format='png',
    #                                                                            initial_marking=initial_marking,
    #                                                                            final_marking=final_marking,
    #                                                                            decorations=None, debug=False,
    #                                                                            set_rankdir=None)
    # pm4py.visualization.common.visualizer.save(viz, "figures/filtered_log_variants.png")

    aligned_traces = alignments.apply_log(log, net, initial_marking, final_marking)
    # print(aligned_traces)
    return


def memory_eval_nfa():
    log = xes_importer.apply(os.path.join("running-example.xes"))
    df_lookup = pd.read_csv("events_mapping.csv", sep=',')

    my_log = []
    for trace in log:
        my_trace = []
        for event in trace:
            if event['concept:name'] in df_lookup.events.values:
                # print('cond met')
                event_in_alphabet = df_lookup.loc[df_lookup['events'] == event['concept:name'], 'mapping'].values[0]
                my_trace.append(event_in_alphabet)
        my_log.append(my_trace)

    for trace in my_log:
        conformance.optimal_alignment_trace_on_nfa(myNfa, trace)

    return


if __name__ == '__main__':
    m_usage_petri = memory_usage(memory_eval_petri)
    print("Memory Usage for Alignment Computation using Petri Net:")
    print(statistics.mean(m_usage_petri))

    m_usage_nfa = memory_usage(memory_eval_nfa)
    print("Memory Usage for Alignment Computation using NFA:")
    print(statistics.mean(m_usage_nfa))
