#!/usr/bin/python


def parse(inp):

  return inp.read()


def get_shortest_path(maze, start, end):

  start = maze.find(start)
  end   = maze.find(end)
  width = maze.find('\n') + 1
  paths = dict()
  visit = set()
  queue = [(start,)]

  while queue:
    path = queue.pop(0)
    curr = path[-1]
    if curr == end: break
    visit.add(curr)
    dirs = (curr - 1, curr + 1, curr - width, curr + width)
    for d in dirs:
      if maze[d] != '#' and d not in visit:
        queue.append(path+(d,))

  node_filt = lambda s:''.join(c for c in s if c.islower() or c == '@')

  path  = ''.join(maze[p] for p in path)
  nodes = node_filt(path)

  for a in nodes:
    for b in nodes[nodes.find(a)+1:]:
      sub   = path[path.find(a):path.find(b)+1]
      doors = ''.join(i for i in sub if i.isupper()
                      if i.lower() not in sub[:sub.find(i)])
      seen  = node_filt(sub)
      paths[seen] = (len(sub)-1, doors)

      sub   = sub[::-1]
      doors = ''.join(i for i in sub if i.isupper()
                      if i.lower() not in sub[:sub.find(i)])
      seen  = node_filt(sub)
      paths[seen] = (len(sub)-1, doors)


  return paths


def get_graph(maze):

  keys  = ''.join(filter(str.islower, maze))
  doors = ''.join(filter(str.isupper, maze))
  paths = dict()

  for a in '@' + keys:
    for b in '@' + keys:
      if a!=b and not any({*p}>={a,b} for p in paths):
        path = get_shortest_path(maze, a, b)
        paths.update(path)

  graph = dict()

  for path, cost in paths.items():
    start = path[0]
    graph[start] = graph.get(start, dict())
    graph[start][path[1:]] = cost

  return graph


def visit_all_nodes(graph, start):

  n_nodes = len(graph)
  queue   = {0:{start}}

  while queue:
    best = min(queue)
    if not queue[best]: queue.pop(best); continue
    path = max(queue[best], key=len)
    queue[best].remove(path)
    if len(set(path)) == n_nodes: return best
    curr = path[-1]
    opts = [node for node, cost in graph[curr].items()
            if node[-1] not in path and set(cost[1].lower()) <= set(path)]
    for option in opts:
      cost = best + graph[curr][option][0]
      if not any(set(p) >= set(path+option) for c,x in queue.items() if c<=cost
                 for p in x):
        queue[cost] = queue.get(cost, set()) | {path+option}


def distributed_visit_all_nodes(graphs, start):

  n_nodes = len(set(node for graph in graphs for node in graph))
  queue   = {0:{(start,) * len(graphs)}}

  while queue:
    best  = min(queue)
    if not queue[best]: queue.pop(best); continue
    paths = max(queue[best], key=lambda p:len(''.join(p)))
    queue[best].remove(paths)
    seen  = set(''.join(paths))
    if len(seen) == n_nodes: return best
    for i, (path, graph) in enumerate(zip(paths, graphs)):
      curr = path[-1]
      opts = [node for node, cost in graph[curr].items()
              if node[-1] not in path and set(cost[1].lower()) <= seen]
      for option in opts:
        cost = best + graph[curr][option][0]
        if not any(set(''.join(p)) >= seen|set(option) for c,x in queue.items()
                   if c<=cost for p in x):
          queue[cost] = queue.get(cost, set()) | {
                        paths[:i]+(path+option,)+paths[i+1:]
                        }


def part_1(data):

  graph = get_graph(data)
  steps = visit_all_nodes(graph, '@')

  return steps


def part_2(data):

  data = list(map(list, data.splitlines()))
  vmid = len(data) // 2
  hmid = len(data[0]) // 2

  data[vmid-1][hmid-1:hmid+2] = ['@','#','@']
  data[vmid  ][hmid-1:hmid+2] = ['#','#','#']
  data[vmid+1][hmid-1:hmid+2] = ['@','#','@']

  tl = get_graph('\n'.join(''.join(row[:hmid+1]) for row in data[:vmid+1]))
  tr = get_graph('\n'.join(''.join(row[hmid:]) for row in data[:vmid+1]))
  bl = get_graph('\n'.join(''.join(row[:hmid+1]) for row in data[vmid:]))
  br = get_graph('\n'.join(''.join(row[hmid:]) for row in data[vmid:]))

  graphs = (tl, tr, bl, br)

  steps  = distributed_visit_all_nodes(graphs, '@')

  return steps


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

