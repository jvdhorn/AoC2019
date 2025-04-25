#!/usr/bin/python


def parse(inp):

  return tuple(map(int, inp.read().strip()))


def group(it, n):

  i = 0
  x = n - 1
  while x < len(it):
    if   i == 0: yield  sum(it[x:x+n])
    elif i == 2: yield -sum(it[x:x+n])
    else       : yield 0
    x += n
    i  = (i + 1) % 4


def fft(inp):

  result = []

  for n in range(len(inp)):
    result.append(abs(sum(group(inp, n+1)))%10)

  return result


def part_1(data):

  for _ in range(100):
    data = fft(data)

  return ''.join(map(str, data[:8]))


def part_2(data):

  data = data * 10000

  return


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

