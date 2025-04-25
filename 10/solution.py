#!/usr/bin/python


def parse(inp):

  grid = set()

  for i, row in enumerate(inp):
    for j, col in enumerate(row.strip()):
      if col == '#': grid.add(complex(i,j))

  return grid


def gcd_reduce(n):

  re = abs(int(n.real))
  im = abs(int(n.imag))

  if 0 in (re, im):
    gcd = max(re, im)
  else:
    gcd = max(i for i in range(1, min(re, im) + 1) if re % i == im % i == 0)

  re = re/gcd if n.real > 0 else -re/gcd
  im = im/gcd if n.imag > 0 else -im/gcd

  return complex(re, im)


def get_best(data):

  best = (0, set())

  for pos in data:
    others = {gcd_reduce(other - pos) for other in data if other != pos}
    best   = max(best, (pos, others), key = lambda x: len(x[1]))

  return best


class Key(complex):

  def __lt__(self, other):

    a = self  / abs(self)
    b = other / abs(other)

    est_a = 2
    est_b = 2
    step  = 1

    while abs(est_a - est_b) < step:

      a_i = est_a - step
      a_j = est_a + step

      if abs(1j ** a_i - a) < abs(1j ** a_j - a):
        est_a = a_i
      else:
        est_a = a_j

      b_i = est_b - step
      b_j = est_b + step

      if abs(1j ** b_i - b) < abs(1j ** b_j - b):
        est_b = b_i
      else:
        est_b = b_j

      step /= 2

    return est_a > est_b


def part_1(data):

  return len(get_best(data)[1])


def part_2(data):

  pos, reduced = get_best(data)
  directions   = sorted(reduced, key=Key)
  link         = dict(zip(directions, directions[1:] + directions[:1]))
  lookup       = dict()

  for item in data - {pos}:
    red         = gcd_reduce(item - pos)
    lookup[red] = lookup.get(red, []) + [item]
    lookup[red].sort(key = lambda x: abs(x - pos))

  count = 200
  drx   = -1

  while count:
    if lookup[drx]:
      count -= 1
      last   = lookup[drx].pop(0)
    drx = link[drx]

  return int(last.real + 100 * last.imag)


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

