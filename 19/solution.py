#!/usr/bin/python


def parse(inp):

  return tuple(map(int, inp.read().split(',')))


class intcode(dict):

  def __init__(self, lst=()):

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

  def process(self):

    while self and (self.stdin or self[self.pos] % 100 != 3):
      self.next()

  def run(self):

    while self:
      self.next()

    return self

  def copy(self):

    instance        = intcode()
    instance.pos    = self.pos
    instance.base   = self.base
    instance.stdin  = self.stdin[:]
    instance.stdout = self.stdout[:]
    instance.update(self)

    return instance


class Beam(object):

  def __init__(self, code):

    self._prog = intcode(code)

  def __call__(self, x, y):

    prog = self._prog.copy()
    prog.stdin = [x,y]
    prog.run()

    return prog.stdout[-1]


def find_outlines(beam, sep):

  for i in range(1, 100):
    x, y = divmod(i, 10)
    if beam(x, y): break

  upper = [(x,y)]
  lower = [(x,y)]

  while upper[-1][0] - lower[-1][0] < sep or lower[-1][1] - upper[-1][1] < sep:

    ux, uy = upper[-1]
    next_u = beam(ux+1, uy)
    if next_u: upper.append((ux+1, uy))
    else     : upper.append((ux, uy+1))

    lx, ly = lower[-1]
    next_l = beam(lx, ly+1)
    if next_l: lower.append((lx, ly+1))
    else     : lower.append((lx+1, ly))

  return upper, lower


def part_1(data):

  beam = Beam(data)
  res  = [beam(x, y) for x in range(50) for y in range(50)]

  return sum(res)


def part_2(data):

  sep          = 100
  beam         = Beam(data)
  upper, lower = find_outlines(beam, sep-1)

  for ux, uy in upper[::-1]:
    for lx, ly in lower[::-1]:
      if ux - lx == ly - uy == sep-1:
        return lx * 10000 + uy


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

