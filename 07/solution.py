#!/usr/bin/python


def parse(inp):

  return tuple(map(int, inp.read().split(',')))


class intcode(list):

  def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)

    self.pos    = 0
    self.stdin  = []
    self.stdout = []

  def add(self, mode):

    op, a, b, out = self[self.pos : self.pos + 4]
    a = a if next(mode) else self[a]
    b = b if next(mode) else self[b]
    self[out]     = a + b
    self.pos     += 4

  def mul(self, mode):

    op, a, b, out = self[self.pos : self.pos + 4]
    a = a if next(mode) else self[a]
    b = b if next(mode) else self[b]
    self[out]     = a * b
    self.pos     += 4

  def inp(self, mode):

    op, out   = self[self.pos : self.pos + 2]
    self[out] = self.stdin.pop(0)
    self.pos += 2

  def out(self, mode):

    op, out = self[self.pos : self.pos + 2]
    out     = out if next(mode) else self[out]
    self.stdout.append(out)
    self.pos += 2

  def jit(self, mode):

    op, a, jmp = self[self.pos : self.pos + 3]
    a          = a   if next(mode) else self[a]
    jmp        = jmp if next(mode) else self[jmp]
    self.pos   = jmp if a != 0 else self.pos + 3

  def jif(self, mode):

    op, a, jmp = self[self.pos : self.pos + 3]
    a          = a   if next(mode) else self[a]
    jmp        = jmp if next(mode) else self[jmp]
    self.pos   = jmp if a == 0 else self.pos + 3

  def ilt(self, mode):

    op, a, b, out = self[self.pos : self.pos + 4]
    a = a if next(mode) else self[a]
    b = b if next(mode) else self[b]
    self[out]     = int(a < b)
    self.pos     += 4

  def eql(self, mode):

    op, a, b, out = self[self.pos : self.pos + 4]
    a = a if next(mode) else self[a]
    b = b if next(mode) else self[b]
    self[out]     = int(a == b)
    self.pos     += 4

  def modes(self, n):

    while True:
      yield n % 10
      n //= 10

  def next(self):

    ops = {1: self.add, 2: self.mul, 3: self.inp, 4: self.out,
           5: self.jit, 6: self.jif, 7: self.ilt, 8: self.eql}

    mode, operation = divmod(self[self.pos], 100)
    ops[operation](self.modes(mode))

    return self[self.pos]

  def run(self):

    while self[self.pos] != 99:
      self.next()

    return self


def perm(iterable):

  iterable = tuple(iterable)

  if len(iterable) == 1:
    yield iterable

  else:
    for i, item in enumerate(iterable):
      for other in perm(iterable[:i] + iterable[i+1:]):
        yield (item,) + other


def part_1(data):

  best = 0

  for order in perm(range(5)):
    signal = 0

    for i in order:
      prog = intcode(data)
      prog.stdin[:] = (i, signal)
      prog.run()
      signal = prog.stdout[0]

    best = max(best, signal)

  return best


def part_2(data):

  best = 0

  for order in perm(range(5,10)):
    curr = 0
    amps = [intcode(data) for _ in order]

    for i, amp in enumerate(amps):
      amp.stdin.append(order[i])
      if i == 0: amp.stdin.append(0)

    while amps[-1][amps[-1].pos] != 99:
      out = len(amps[curr].stdout)

      while len(amps[curr].stdout) == out:
        amps[curr].next()

      amps[(curr + 1) % 5].stdin.append(amps[curr].stdout[-1])
      curr = (curr + 1) % 5

    best = max(best, amps[-1].stdout[-1])

  return best


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

