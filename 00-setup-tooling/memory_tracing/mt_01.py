import tracemalloc

tracemalloc.start()

# your code here
# model = build_model()
# data = load_dataset()

import numpy as np

# create a large numpy array
large_array = np.ones(10000)

# create a list of large objects
large_objects = [np.ones(10000) for _ in range(10)]

# create a dictionary of large objects
large_dictionary = {str(i): np.ones(10000) for i in range(10)}

# create a list of lists of large objects
large_list_of_lists = [[np.ones(10000) for _ in range(10)] for _ in range(10)]




snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
for stat in top_stats[:10]:
    print(stat)

print("\n\n\n")

top_stats = snapshot.statistics("traceback")
for stat in top_stats[:10]:
    print(stat)

print("\n\n\n")

top_stats = snapshot.statistics("filename")
for stat in top_stats[:10]:
    print(stat)

