#!/usr/bin/python


def parse(inp):

  a, b = map(int, inp.read().split('-'))

  return range(a, b+1)


def check(n):

  return n == ''.join(sorted(n)) and any(c * 2 in n for c in n)


def check_2(n):

  counts = any(n[i+1:i+2] == c and c not in n[i-1:i]+n[i+2:i+3]
               for i, c in enumerate(n))

  return n == ''.join(sorted(n)) and counts


def part_1(data):

  return sum(check(n) for n in map(str, data))


def part_2(data):

  return sum(check_2(n) for n in map(str, data))


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

