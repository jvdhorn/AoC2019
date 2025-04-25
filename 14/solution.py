#!/usr/bin/python


def parse(inp):

  conv = dict()

  for ln in inp:
    ln           = ln.replace('=>', ' ').replace(',',' ')
    *inp, out    = ((x, int(n)) for n, x in zip(*[iter(ln.split())]*2))
    conv[out[0]] = (out[1], tuple(inp))

  return conv


def ceildiv(a, b):

  return -(a // -b)


def dependencies(tree):

  dep = {item: set() for item in tree}
  dep.update(ORE=set())

  for item in tree:
    queue = {item}

    while queue:
      curr = queue.pop()

      for other, _ in tree[curr][1]:
        if other != 'ORE':
          dep[item].add(other)
          queue.add(other)

  return dep


def simulate(data, fuel):

  queue = {'FUEL': fuel}
  dep   = dependencies(data)

  while queue:
    curr = sorted(queue, key = lambda x: -len(dep[x]))[0]
    need = queue.pop(curr)

    if curr == 'ORE':
      return need

    else:
      yld, res = data[curr]

      for other, i in res:
        queue[other] = queue.get(other, 0) + i * ceildiv(need, yld)


def part_1(data):

  return simulate(data, 1)


def part_2(data):

  limit = 10 ** 12
  fuel  = 0
  var   = 1

  while True:
    ore = simulate(data, fuel + var)

    if ore < limit:
      var *= 2
    elif var == 1:
      return fuel
    else:
      fuel += var // 2
      var   = 1


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

