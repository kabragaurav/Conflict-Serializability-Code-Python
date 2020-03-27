# ADT Assignment#3

__author__ = "Gaurav Kabra"

'''
Write a Program which shall read a concurrent schedule involving n transactions with read and write instructions on data items 
from an input file (sample input file attached) and find whether the schedule is Conflict Serializable or not using the graph-based 
method discussed in the class. In case of conflict serializable schedule, your program shall also give the serializability order 
as well and for non-serializable schedule, give the cycle(s) present in the graph.The sample input contains 3 transactions (T1, T2, T3) 
and 3 data items (A, B, C) however your program shall be able to handle any finite number of transactions and data items. 
There shall not be any constraints on number of transactions and data items.
'''


from cycle_detector import Graph
# from cycle_printer import *
from cycle_printer import *

# This dict will be used in printing cycles (if present)
# We will send it to cycle_printer module
graph = {}   

try:
    def isConflicting(instruction1, instruction2):
        if instruction1 == "VACANT" or instruction2 == "VACANT":
            return False
        oper1, oper2 = instruction1[0], instruction2[0]
        data_item1, data_item2 = instruction1[2], instruction2[2]
        if oper1 == "W" or oper2 == "W":
            if data_item1 == data_item2:
                return True
        return False


    file_name = input("Enter complete file path e.g. './/Inputs//input.txt'")

    # read file
    # and find how many trans ie vertices in graph
    with open(file_name) as f:
        first_line = f.readline().split(":")
        no_of_transactions = len(first_line[1].split(','))

    # make 2-d array of lists for different transactions
    ls = [[] for _ in range(no_of_transactions)]

    # now populate these lists

    with open(file_name) as f:
        # skip first 3 lines
        for _ in range(3):
            temp = f.readline()
        line = f.readline()
        while line:
            level1 = line.split(":")
            transaction_no = int(level1[0][1])  # e.g. extract 1 from T1
            count = 0
            for _ in range(len(ls)):
                if _ == transaction_no-1:
                    ls[_].append(level1[1][:-2])
                else:
                    ls[_].append("VACANT")
            line = f.readline()

    # PRINT WHOLE SCHEDULE, S
    print("####################### SCHEDULE : #########################")
    for individual_list in ls:
        print(individual_list)
    


    # Now create a directed graph
    g = Graph(no_of_transactions)
    # Edge is added as Ti->Tj when Ti and Tj
    # operate on same data-type and at least one operation is W
    L = len(ls[0])     # length of transactions
    for transaction_id in range(no_of_transactions):
        for i in range(L):
            instruction = ls[transaction_id][i]
            for j in range(no_of_transactions):
                if j == transaction_id:
                    continue
                else:
                    for k in range(i+1,L):
                        if isConflicting(instruction, ls[j][k]):
                            g.addEdge(transaction_id,j)
                            if transaction_id not in graph.keys():
                                graph[transaction_id] = [j]
                            else:
                                graph[transaction_id].append(j)
    print("######################## RESULT: ###################################")
    if g.isCyclic():
        print("NOT Conflict Serializable.")
        print("######################## Cycle(s): ######################")
        cycle_printing_fn(graph)
    else:
        print("Conflict Serializable")
        print("#################### Order of execution (Topological Sort) #######################")
        order = g.topologicalSort()
        for item in order:
            print("T"+str(item+1),end='->')
except:
    print("There is error in Input file format!")
