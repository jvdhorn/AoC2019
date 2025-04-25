#!/usr/bin/python


def parse(inp):

  return [int(ln) for ln in inp]


def fuel(n):

  return max(0, n // 3 - 2)


def recur_fuel(n):

  return n and fuel(n) + recur_fuel(fuel(n))


def part_1(data):

  return sum(map(fuel, data))


def part_2(data):

  return sum(map(recur_fuel, data))


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

