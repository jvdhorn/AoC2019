#!/usr/bin/python


def parse(inp):

  drc = {'R':1, 'D':-1j, 'L':-1, 'U':1j}

  return [[drc[i[0]] * int(i[1:]) for i in ln.strip().split(',')] for ln in inp]


def accumulate(wire):

  trace = [0]

  for d in wire:
    if d.real:
      step = -1 if d.real < 0 else 1
      trace += [trace[-1] + i for i in range(step, int(d.real) + step, step)]
    elif d.imag:
      step = -1 if d.imag < 0 else 1
      trace += [trace[-1] + i * 1j for i in range(step, int(d.imag) + step, step)]

  return trace


def part_1(data):

  a, b = map(accumulate, data)

  return min(int(abs(i.real) + abs(i.imag)) for i in set(a) & set(b) if i != 0)


def part_2(data):

  a, b = map(accumulate, data)

  return min(a.index(i) + b.index(i) for i in set(a) & set(b) if i != 0)


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

