import numpy as np


# Makes a matrix representing the colored graph
# param n: int representing the size of the graph
# param r: Bool for whether to use a random solver or not
def solver(n, r=None):
    m = np.zeros((n, n), dtype=int)
    # random solver
    if r:
        rm = np.random.randint(3, size=(n, n))
        for i in range(1, n):
            for j in range(i):
                m[i, j] = rm[i, j]

    # non-random solver. Currently no algorithm in place
    else:
        m[1, 0] = 2
    return m


# counts the number of monochromatic triangles in the graph
def counter(m):
    n = len(m)
    count = 0
    tot = 0

    for a in range(n):
        for b in range(a+1, n):
            for c in range(b+1, n):
                tot += 1
                # print('looking at this triangle: ', a, b, c)
                if (m[b, a] == m[c, a]) and (m[b, a] == m[c, b]):
                    # print('adding onto current c. c = ', count)
                    count += 1

    return count, tot


# Takes a list of strings and concatenates them to one string, each element separated by ', '
def to_string(list_of_strings):
    concat_string = ''
    for l in list_of_strings:
        concat_string += l + ', '
    return concat_string


# Stores a result file at path. First line is number of monotris. Second line is the result string of the colored graph.
# If there is already a file at path it will be overwritten.
# param path: string for where to store results. "results/X.txt" where X is the size of the Graph
# param result_string: string representing the graph coloring
# param mcts: int representing the number of monochromatic triangles in the colored graph
def my_write(path, result_string, mcts):
    content = str(mcts) + '\n' + to_string(result_string)
    file = open(path, "w")
    file.write(content)
    file.close()


# If the number of monotris is lower than the recorded number for the given size the
# result_string number of monotris is saved to file named 'size'.txt in the results folder
def store_results(size, result_string, monotris):
    path = "results/" + str(size) + ".txt"

    try:
        file = open(path, "r")
        content = file.readlines()
        file.close()

        if len(content) == 2:
            ref = int(content[0])
            if monotris < ref:
                print('found new best score of: ', monotris, ' for size: ', n)
                my_write(path, result_string, monotris)
            else:
                print('did not beat old solution of: ', ref, ' for size: ', n)
        else:
            print('Weird file at path: ', path)
    except IOError:
        print('did not find file at path: ', path, '. Creating a new one')
        my_write(path, result_string, monotris)


def main(n):
    color_matrix = solver(n, r=True)
    # color_matrix = solver(n)
    print('solution matrix:')
    print(color_matrix)
    result = []

    for i in range(1, n):
        arcs = ''
        for j in range(i):
            arcs = arcs + str(color_matrix[i, j])
        result.append(arcs)

    mono_tris, tot_tris = counter(color_matrix)
    print('monochromatic triangles = ', mono_tris, ', total triangles = ', tot_tris)
    return result, mono_tris


# make the code run for lists
n = 17
res, score = main(n)
print('solution string: ', res)

store_results(n, res, score)
