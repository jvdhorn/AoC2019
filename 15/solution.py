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


def explore(data, cache = dict()):

  if data in cache:
    return cache[data]

  drx     = {1: 1j, 2: -1j, 3: -1, 4: 1}
  prog    = intcode(data)
  queue   = [(prog,())]
  visited = cache[data] = {0:1}

  while queue:
    curr, inp = queue.pop(0)

    for d in 1, 2, 3, 4:
      pos  = sum(drx.get(i) for i in inp + (d,))
      prog = curr.copy()
      prog.stdin.append(d)
      prog.process()

      if prog.stdout[-1]:
        if pos not in visited:
          queue.append((prog,inp+(d,)))
        visited[pos] = prog.stdout[-1]

  return visited


def trace(tree, start, end = None):

  queue   = [(start,)]
  visited = set()

  while queue:
    curr = queue.pop(0)
    visited.add(curr[-1])

    if curr[-1] == end:
      break

    for d in 1j, -1j, -1, 1:
      nxt = curr[-1] + d

      if nxt in tree and nxt not in visited:
        queue.append(curr + (nxt,))

  return len(curr) - 1


def part_1(data):

  tree = explore(data)
  end  = next(node for node in tree if tree[node] == 2)

  return trace(tree, 0, end)


def part_2(data):

  tree  = explore(data)
  start = next(node for node in tree if tree[node] == 2)

  return trace(tree, start)


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

