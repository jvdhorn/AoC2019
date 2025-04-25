#!/usr/bin/python


def parse(inp):

  return tuple(map(int, inp.read().split(',')))


class intcode(dict):

  def __init__(self, lst):

    super().__init__(enumerate(lst))

    self.pos    = 0
    self.base   = 0
    self.stdin  = []
    self.stdout = []

  def __getitem__(self, key):

    return super().get(key, 0)

  def add(self, read):

    a, b, out = (next(read) for _ in range(3))
    self[out] = self[a] + self[b]
    self.pos += 4

  def mul(self, read):

    a, b, out = (next(read) for _ in range(3))
    self[out] = self[a] * self[b]
    self.pos += 4

  def inp(self, read):

    out       = next(read)
    self[out] = self.stdin.pop(0)
    self.pos += 2

  def out(self, read):

    val       = next(read)
    self.stdout.append(self[val])
    self.pos += 2

  def jit(self, read):

    a, jmp   = (next(read) for _ in range(2))
    self.pos = self[jmp] if self[a] != 0 else self.pos + 3

  def jif(self, read):

    a, jmp   = (next(read) for _ in range(2))
    self.pos = self[jmp] if self[a] == 0 else self.pos + 3

  def ilt(self, read):

    a, b, out = (next(read) for _ in range(3))
    self[out] = int(self[a] < self[b])
    self.pos += 4

  def eql(self, read):

    a, b, out = (next(read) for _ in range(3))
    self[out] = int(self[a] == self[b])
    self.pos += 4

  def baj(self, read):

    base       = next(read)
    self.base += self[base]
    self.pos  += 2

  def reader(self, key):

    pos = self.pos

    while True:
      pos      += 1
      key, mode = divmod(key, 10)
      if   mode == 0: yield self[pos]
      elif mode == 1: yield pos
      elif mode == 2: yield self[pos] + self.base

  def next(self):

    ops = {1: self.add, 2: self.mul, 3: self.inp, 4: self.out,
           5: self.jit, 6: self.jif, 7: self.ilt, 8: self.eql,
           9: self.baj}

    key, operation = divmod(self[self.pos], 100)
    ops[operation](self.reader(key))

    return self[self.pos]

  def run(self):

    while self[self.pos] != 99:
      self.next()

    return self


def simulate(data, col):

  prog  = intcode(data)
  pos   = 0
  drx   = 1j
  tiles = {pos:col}

  while prog[prog.pos] != 99:
    prog.stdin.append(tiles.get(pos, 0))
    out = len(prog.stdout)

    while prog[prog.pos] != 99 and len(prog.stdout) < out + 2:
      prog.next()

    col, turn  = prog.stdout[-2:]
    tiles[pos] = col
    drx        = drx * -1j if turn else drx * 1j
    pos       += drx

  return tiles


def vis(grid):

  re     = {int(x.real) for x in grid}
  im     = {int(x.imag) for x in grid}
  result = ''

  for x in range(max(im), min(im) - 1 , -1):
    for y in range(min(re), max(re) + 1):
      result += '.#'[complex(y,x) in grid]
    result += '\n'

  return result.strip()


def part_1(data):

  return len(simulate(data, 0))


def part_2(data):

  tiles  = simulate(data, 1)
  grid   = {tile for tile in tiles if tiles[tile]}
  result = vis(grid)

  return result


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

