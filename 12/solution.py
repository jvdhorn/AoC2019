#!/usr/bin/python


def parse(inp):

  moons = set()

  for ln in inp:
   moons.add(tuple(int(coord.strip('<xyz=> \n')) for coord in ln.split(',')))

  return moons


def cmp(a, b):

  return -1 if a < b else 1 if a > b else 0


def simulate(inp, steps=float('inf')):

  moons  = [[list(moon), [0,0,0]] for moon in inp]
  states = set()

  while len(states) < steps:

    state = hash(tuple(sum(sum(moons,[]),[])))
    if state in states: steps = len(states)
    states.add(state)

    for first, velo in moons:
      for second, _ in moons:
        velo[:] = map(int.__add__, velo, map(cmp, second, first))

    for moon, velo in moons:
      moon[:] = map(int.__add__, moon, velo)

  energy = sum(sum(map(abs, p)) * sum(map(abs, v)) for p, v in moons)

  return energy, steps


def sim1d(inp, steps=float('inf')):

  moons  = list(inp)
  velos  = [0] * len(moons)
  states = set()

  while len(states) < steps:

    state    = hash(tuple(moons + velos))
    if state in states: steps = len(states)
    states.add(state)

    diff     = (sum(cmp(other, moon) for other in moons) for moon in moons)
    velos[:] = map(int.__add__, velos, diff)
    moons[:] = map(int.__add__, moons, velos)

  return steps


def lcm(arr):

  curr, *arr = arr

  while arr:
    nxt  = arr.pop()
    curr = next(curr * n for n in range(1, nxt+1) if (curr * n) % nxt == 0)

  return curr


def part_1(data):

  return simulate(data, 1000)[0]


def part_2(data):

  steps = map(sim1d, zip(*data))

  return lcm(steps)


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

