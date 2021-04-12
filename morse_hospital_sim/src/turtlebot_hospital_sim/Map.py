from copy import deepcopy

coords = {}
graph = {"Respiratory Control": ["IC Corridor"],
         "IC Corridor": ["IC Room 1", "IC Room 2", "IC Room 3", "IC Room 4",
                         "IC Room 5", "IC Room 6", "IC Room 7", "PC Corridor",
                         "Respiratory Control"],
         "IC Room 1": ["IC Corridor"],
         "IC Room 2": ["IC Corridor"],
         "IC Room 3": ["IC Corridor"],
         "IC Room 4": ["IC Corridor"],
         "IC Room 5": ["IC Corridor"],
         "IC Room 6": ["IC Corridor"],
         "IC Room 7": ["IC Corridor"],
         "PC Corridor": ["PC Room 1", "PC Room 2", "PC Room 3", "PC Room 4",
                         "PC Room 5", "PC Room 6", "PC Room 7", "PC Room 8",
                         "PC Room 9", "PC Room 10",
                         "IC Corridor", "Pharmacy Corridor"],
         "PC Room 1": ["PC Corridor"],
         "PC Room 2": ["PC Corridor"],
         "PC Room 3": ["PC Corridor"],
         "PC Room 4": ["PC Corridor"],
         "PC Room 5": ["PC Corridor"],
         "PC Room 6": ["PC Corridor"],
         "PC Room 7": ["PC Corridor"],
         "PC Room 8": ["PC Corridor"],
         "PC Room 9": ["PC Corridor"],
         "PC Room 10": ["PC Corridor"],
         "Pharmacy Corridor": ["Reception", "PC Corridor", "Pharmacy"],
         "Reception": ["Pharmacy Corridor"],
         "Pharmacy": ["Pharmacy Corridor"]}


def get_path(start, end):
    #return [coords[node] for node in dfs(start, end)]
    return dfs(start, end)


def dfs(start, end, visited=set(), path=[]):
    if start not in visited:
        visited.add(start)
        if start == end:
            return True
        for node in graph[start]:
            if dfs(node, end, visited, path):
                path.insert(0, node)
                break
        return path


print(get_path("Respiratory Control", "Pharmacy"))
