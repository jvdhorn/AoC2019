#!/usr/bin/python


def parse(inp):

  return tuple(map(int, inp.read().split(',')))


def intcode(code):

  ops = {1: int.__add__, 2: int.__mul__}
  code = list(code)
  pos = 0

  while code[pos] != 99:
    op, a, b, out = code[pos:pos+4]
    code[out]     = ops[op](code[a], code[b])
    pos          += 4

  return code


def part_1(data):

  data = data[:1] + (12, 2) + data[3:]

  return intcode(data)[0]


def part_2(data):

  for i in range(100):
    for j in range(100):
      data = data[:1] + (i, j) + data[3:]

      if intcode(data)[0] == 19690720:
        return 100 * i + j


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

