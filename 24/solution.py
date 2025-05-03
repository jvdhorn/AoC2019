#!/usr/bin/python


def parse(inp):

  grid = set()

  for i, row in enumerate(inp):
    for j, col in enumerate(row):
      if col == '#': grid.add(complex(i,j))

  return grid


def evolve(grid):

  outer = {0: ((0, 1j), (0, 1), (1, 2j+1), (1, 1j+2)),
           1j: ((0, 0), (0, 2j), (0,1j+1), (1, 2j+1)),
           2j: ((0, 1j), (0, 3j), (0, 2j+1), (1, 2j+1)),
           3j: ((0, 2j), (0, 4j), (0, 3j+1), (1, 2j+1)),
           4j: ((0, 3j), (0, 4j+1), (1, 2j+1), (1, 3j+2)),
           4j+1: ((0, 4j), (0, 3j+1), (0, 4j+2), (1, 3j+2)),
           4j+2: ((0, 4j+1), (0, 4j+3), (0, 3j+2), (1, 3j+2)),
           4j+3: ((0, 4j+2), (0, 4j+4), (0, 3j+3), (1, 3j+2)),
           4j+4: ((0, 4j+3), (0, 3j+4), (1, 3j+2), (1, 2j+3)),
           3j+4: ((0, 2j+4), (0, 4j+4), (0, 3j+3), (1, 2j+3)),
           2j+4: ((0, 1j+4), (0, 3j+4), (0, 2j+3), (1, 2j+3)),
           1j+4: ((0, 4), (0, 2j+4), (0, 1j+3), (1, 2j+3)),
           4: ((0, 3), (0, 1j+4), (1, 2j+3), (1, 1j+2)),
           3: ((0, 2), (0, 4), (0, 1j+3), (1, 1j+2)),
           2: ((0, 1), (0, 3), (0, 1j+2), (1, 1j+2)),
           1: ((0, 0), (0, 1j+1), (0, 2), (1, 1j+2))}

  inner = {1j+1: ((0, 1j), (0, 1), (0, 1j+2), (0, 2j+1)),
           2j+1: ((0, 1j+1), (0, 3j+1), (0, 2j), (-1, 0),
                  (-1, 1j), (-1, 2j), (-1, 3j), (-1, 4j)),
           3j+1: ((0, 4j+1), (0, 2j+1), (0, 3j), (0, 3j+2)),
           3j+2: ((0, 3j+1), (0, 3j+3), (0, 4j+2), (-1, 4j),
                  (-1, 4j+1), (-1, 4j+2), (-1, 4j+3), (-1, 4j+4)),
           3j+3: ((0, 2j+3), (0, 4j+3), (0, 3j+2), (0, 3j+4)),
           2j+3: ((0, 1j+3), (0, 3j+3), (0, 2j+4), (-1, 4j+4),
                  (-1, 3j+4), (-1, 2j+4), (-1, 1j+4), (-1, 4)),
           1j+3: ((0, 3), (0, 2j+3), (0, 1j+4), (0, 1j+2)),
           1j+2: ((0, 2), (0, 1j+1), (0, 1j+3), (-1, 4),
                  (-1, 3), (-1, 2), (-1, 1), (-1, 0))}

  neighbours = outer.copy()
  neighbours.update(inner)

  new_grid  = set()
  potential = set()

  for level, pos in grid:
    nb = {(level+lvl, p) for lvl, p in neighbours[pos]}
    potential |= nb - grid
    if len(nb & grid) == 1: new_grid.add((level, pos))

  for level, pos in potential:
    nb = {(level+lvl, p) for lvl, p in neighbours[pos]}
    if len(nb & grid) in (1,2): new_grid.add((level, pos))
    
  return new_grid


def part_1(data):

  seen = set()
  curr = frozenset(data)

  while curr not in seen:
    nxt = set()
    for i in range(5):
      for j in range(5):
        pos = complex(i,j)
        adj = {pos+1, pos-1, pos+1j, pos-1j} & curr
        if len(adj) == 1 and pos in curr: nxt.add(pos)
        elif len(adj) in (1,2) and pos not in curr: nxt.add(pos)
    seen.add(frozenset(curr))
    curr = nxt

  return int(sum(2**(i.imag + 5 * i.real) for i in curr))


def part_2(data):

  grid = {(0, pos) for pos in data}

  for _ in range(200):
    grid = evolve(grid)

  return len(grid)


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

