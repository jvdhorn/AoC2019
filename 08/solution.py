#!/usr/bin/python


def parse(inp):

  data   = tuple(map(int, inp.read().strip()))
  x, y   = {12: (2,3), 16: (2,2)}.get(len(data), (6,25))
  layers = tuple(zip(*[zip(*[iter(data)] * y)] * x))

  return layers


def part_1(data):

  counters = tuple(sum(layer, ()).count for layer in data)

  return min((count(0), count(1) * count(2)) for count in counters)[1]


def part_2(data):

  return '\n'.join(''.join('.#'[next(i for i in col if i < 2)]
                           for col in zip(*row)) for row in zip(*data))


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

