#!/usr/bin/python


def parse(inp):

  return inp.read()


def retrieve_labels(maze):

  width  = maze.find('\n')+1
  labels = dict()

  for i, char in enumerate(maze):
    if char == '.':
      opts = list(filter(str.isalpha, (maze[i-2:i], maze[i+1:i+3],
              maze[i-width]+maze[i-width*2], maze[i+width]+maze[i+width*2])))
      if opts: labels[i] = ''.join(sorted(opts[0]))

  return labels


def flood(maze, start, dest, allowed='.'):

  width = maze.find('\n')+1

  queue = [(start,)]
  visit = set()
  paths = dict()

  while queue:
    curr = queue.pop(0)
    pos  = curr[-1]
    if pos in visit or maze[pos] not in allowed: continue
    visit.add(pos)
    for d in (pos-1, pos+1, pos-width, pos+width):
      if d in dest:
        paths[(start,d)] = len(curr) + 1
      queue.append(curr+(d,))

  return paths


def get_graph(maze):

  labels = retrieve_labels(maze)
  paths  = dict()

  for label in labels:
    paths.update(flood(maze, label, set(labels)-{label}))

  graph = dict()

  for (a, b), dist in paths.items():
    a_label = labels[a]
    b_label = labels[b]
    graph[a_label] = graph.get(a_label, dict())
    graph[a_label][b_label] = dist

  return graph


def get_fancy_graph(maze):

  labels = retrieve_labels(maze)
  paths  = dict()

  for label in labels:
    paths.update(flood(maze, label, set(labels)-{label}))

  clean  = ''.join((c+' ')[c.isalpha()] for c in maze)
  inner  = set(sum(flood(clean, len(maze)//2, set(labels), ' '),()))

  graph = dict()

  for (a, b), dist in paths.items():
    a_label = labels[a] + 'oi'[a in inner]
    a_label_alt = labels[a] + 'io'[a in inner]
    b_label = labels[b] + 'oi'[b in inner]
    graph[a_label] = graph.get(a_label, dict())
    graph[a_label][b_label] = (dist - 1, 0)
    if a_label_alt not in ('AAi', 'ZZi'):
      graph[a_label][a_label_alt] = (1, 1 if a in inner else -1)

  return graph


def find_path(graph, start, dest):

  queue = {0:{(start,)}}

  while queue:
    best = min(queue)
    if not queue[best]: queue.pop(best); continue
    path = queue[best].pop()
    curr = path[-1]
    if curr == dest: return best - 1
    opts = [node for node in graph[curr] if node not in path]
    for option in opts:
      cost = best + graph[curr][option]
      if not any(set(p) >= set(path+(option,)) for c,x in queue.items() if c<=cost
                 for p in x):
        queue[cost] = queue.get(cost, set()) | {path+(option,)}


def find_recursive_path(graph, start, dest):

  queue = {0:[(start,0)]}
  visit = set()

  while queue:
    best = min(queue)
    if not queue[best]: queue.pop(best); continue
    curr, lvl = queue[best].pop(0)
    visit.add((curr, lvl))
    for node in graph[curr]:
      cost  = best + graph[curr][node][0]
      level = lvl  + graph[curr][node][1]
      if (node, level) == (dest, 0): return cost
      elif (node, level) not in visit and level >= 0:
        queue[cost] = queue.get(cost, list()) + [(node, level)]



def part_1(data):

  graph = get_graph(data)
  path  = find_path(graph, 'AA', 'ZZ')

  return path


def part_2(data):

  graph = get_fancy_graph(data)
  path  = find_recursive_path(graph, 'AAo', 'ZZo')

  return path


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

