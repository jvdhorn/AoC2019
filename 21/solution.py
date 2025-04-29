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


def part_1(data):

  prog = intcode(data)
  inst = 'NOT C J\nAND D J\nNOT A T\nOR T J\nWALK\n'
  prog.stdin = list(map(ord, inst))
  prog.run()

  return prog.stdout[-1]


def part_2(data):

  'D AND (E OR H) AND NOT (A AND B AND C)'

  raw = '''
  OR C J
  AND B J
  AND A J
  NOT J J
  OR H T
  OR E T
  AND T J
  AND D J
  RUN
  '''

  prog = intcode(data)
  inst = '\n'.join(line.strip() for line in raw.strip().splitlines())+'\n'
  prog.stdin = list(map(ord, inst))
  prog.run()

  return prog.stdout[-1]


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

