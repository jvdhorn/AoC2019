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

  def __bool__(self):

    return self[self.pos] != 99

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
    if self: ops[operation](self.reader(key))

    return self[self.pos]

  def run(self):

    while self:
      self.next()

    return self


def vis(tiles):

  re     = [int(x.real) for x in tiles]
  im     = [int(x.imag) for x in tiles]
  result = '\033[H\033[J' # This clears the console before printing

  for j in range(min(im), max(im)+1):
    for i in range(min(re), max(re)+1):
      result += ' #+_o'[tiles.get(complex(i,j), 0)]
    result += '\n'

  return result


def get_state(inp):

  tiles = {complex(x,y): b for x, y, b in zip(*[iter(inp)]*3)}
  score = tiles.pop(-1) if -1 in tiles else None

  return tiles, score


def part_1(data):

  prog = intcode(data)
  prog.run()

  return prog.stdout[2::3].count(2)

def part_2(data):

  prog  = intcode((2,) + data[1:])
  tiles = dict()

  while prog:
    while prog and (prog[prog.pos] % 100 != 3 or prog.stdin): prog.next()
    new_tiles, score = get_state(prog.stdout)
    tiles.update(new_tiles)
    prog.stdout.clear()
    ball = next(tile for tile in tiles if tiles[tile] == 4)
    padd = next(tile for tile in tiles if tiles[tile] == 3)
    prog.stdin.append(-1 if ball.real < padd.real else ball.real > padd.real)

    for _ in range(0): print(end=vis(tiles))

  return score


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

