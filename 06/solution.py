#!/usr/bin/python


def parse(inp):

  graph = dict()

  for ln in inp:
    a, b     = ln.strip().split(')')
    graph[a] = graph.get(a, frozenset()) | {b}

  return graph


def get_paths(graph):

  paths = set()
  queue = {('COM',)}

  while queue:
    path = queue.pop()

    if path[-1] not in graph:
      paths.add(path)

    else:
      for node in graph[path[-1]]:
        queue.add(path + (node,))

  return paths


def part_1(data):

  paths  = get_paths(data)
  unique = set()

  for path in paths:
    for i, first in enumerate(path):
      for second in path[i+1:]:
        unique.add((first, second))

  return len(unique)


def part_2(data):

  paths = get_paths(data)
  a, b  = (set(path) for path in paths if path[-1] in ('YOU', 'SAN'))

  return len(a^b) - 2


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

