# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

from execution_time import ExecutionTime
from operator import itemgetter
from collections import Counter

e = ExecutionTime()

@e.timeit
def find_who_should_change(P, T):
    people = [idx for idx, p in enumerate(P) if p != T[idx]]
    if len(people) == 0:
        return [], 0, 0
    elif len(people) == 1:
        return people, 1, 0
    else:
        pets_received_wrong_present = itemgetter(*people)(P)
        pets_counter = Counter(pets_received_wrong_present)
        D_num = pets_counter[1]
        C_num = pets_counter[2]
        return set(people), D_num, C_num


@e.timeit
def create_graph(A, B):
    graph = {}
    for idx, _ in enumerate(A):
        if A[idx] in graph:
            graph[A[idx]].append(B[idx])
        else:
            graph[A[idx]] = [B[idx]]
        if B[idx] in graph:
            graph[B[idx]].append(A[idx])
        else:
            graph[B[idx]] = [A[idx]]
    return graph

@e.timeit
def get_subgraph(graph, subgraph_vertices, vert_to_check):
    for el in vert_to_check:
        if el in subgraph_vertices:
            continue
        else:
            subgraph_vertices.append(el)
            if el in graph:
                new_vert_to_check = graph[el]
                get_subgraph(graph, subgraph_vertices, new_vert_to_check)


@e.timeit
def get_all_connected_components(graph):
    # get all subgraphs
    list_of_subgraphs = []
    all_checked_vertices = set()

    for _, vertix in enumerate(graph.keys()):
        if vertix not in all_checked_vertices:
            subgraph = {vertix}
            vert_to_check = set(graph[vertix])
            all_checked_vertices.add(vertix)
            while len(vert_to_check) > 0:
                el = vert_to_check.pop()
                all_checked_vertices.add(el)
                if not subgraph.issubset({el}):
                    subgraph.add(el)
                    elements_to_add = filter(lambda x: x not in all_checked_vertices and x not in vert_to_check, graph[el])
                    for e in elements_to_add:
                        vert_to_check.add(e)
            list_of_subgraphs.append(subgraph)
    return list_of_subgraphs


@e.timeit
def if_people_who_should_make_exchange_are_paired(subgraph_vertices, people_ids, P):
    q = Counter([P[el] for el in set(subgraph_vertices).intersection(people_ids)])
    D_num = q[1]
    C_num = q[2]
    if D_num == C_num:
        return True
    else:
        return False

@e.timeit
def solution(P, T, A, B):
    people_ids, D_num, C_num = find_who_should_change(P, T)
    if len(people_ids) == 0:
        return True
    if len(A) == 0 or len(B) == 0 or D_num != C_num:
        return False
    else:
        graph = create_graph(A, B)
        list_of_subgraphs = get_all_connected_components(graph)

        for subgraph in list_of_subgraphs:
            res = if_people_who_should_make_exchange_are_paired(subgraph, people_ids, P)
            if not res:
                return False
        return True


# Test the solution

# Correctness tests
print(solution([1, 1, 2], [1, 1, 1], [0, 2], [1, 1]))
print(solution([1, 1, 2], [2, 1, 1], [0, 2], [1, 1]))
print(solution([1, 1, 2], [1, 1, 2], [0, 2], [1, 1]))
print(solution([1, 1, 2], [2, 1, 1], [0, 1], [1, 1]))
print(solution([1], [1], [], []))
print(solution([1, 1, 2, 2, 1, 1, 2, 2], [1, 1, 1, 1, 2, 2, 2, 2], [0, 2, 4, 6], [1, 3, 5, 7]))
print(solution([2, 2, 2, 2, 1, 1, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2], [0, 1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7]))

# Performance tests
list_with_pets = [1, 2]
test_P = [1]*50000 + [2]*50000
test_T = [2]*50000 + [1]*50000
test_A = [el for el in range(1, 200000)]
test_B = [el+1 for el in range(1, 200000)]
print(solution(test_P, test_T, test_A, test_B))


# Print stats
q = e.logtime_data
for func, params in q.items():
    print(func, ": ")
    for param_name, param_value in params.items():
        print(f"\t{param_name} - {param_value}")
