# Format: "Name": [x_coord, y_coord]
coords = {"Respiratory Control": [-37, 35],
          "IC Corridor": [-37, 15],
          "IC Room 1": [-38, 35],
          "IC Room 2": [-34, 35],
          "IC Room 3": [-38, 23],
          "IC Room 4": [-34, 17.5],
          "IC Room 5": [-38, 21.5],
          "IC Room 6": [-38, 10],
          "PC Corridor": [-19, 16],
          "PC Room 1": [-28.5, 18],
          "PC Room 2": [-27.4, 18],
          "PC Room 3": [-21, 18],
          "PC Room 4": [-19, 18],
          "PC Room 5": [-13.5, 18],
          "PC Room 6": [-11.5, 18],
          "PC Room 7": [-4, 18],
          "PC Room 8": [-27, 13],
          "PC Room 9": [-26, 13],
          "PC Room 10": [-18, 13],
          "Reception": [-1, 20],
          "Pharmacy Corridor": [0, 8],
          "Pharmacy": [-2, 2.6]}

graph = {"Respiratory Control": ["IC Corridor"],
         "IC Corridor": ["IC Room 1", "IC Room 2", "IC Room 3", "IC Room 4",
                         "IC Room 5", "IC Room 6", "PC Corridor",
                         "Respiratory Control"],
         "IC Room 1": ["IC Corridor"],
         "IC Room 2": ["IC Corridor"],
         "IC Room 3": ["IC Corridor"],
         "IC Room 4": ["IC Corridor"],
         "IC Room 5": ["IC Corridor"],
         "IC Room 6": ["IC Corridor"],
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
    path = dfs(start, end)
    return path, {node: coords[node] for node in path}


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
