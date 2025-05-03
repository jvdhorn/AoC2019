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


class Interface(intcode):

  def command(self, inp):

    self.stdout.clear()
    self.stdin += list(map(ord, inp + '\n'))
    self.process()

    return ''.join(map(chr, self.stdout))


def parse_view(view):

  name  = ''
  doors = set()
  items = set()

  for lst in view.strip().split('\n\n'):
    if '==' in lst:
      if not name: name = lst.split('==')[1].strip()
      else       : break
    if 'Doors here' in lst: doors |= {x.strip('- ') for x in lst.splitlines()[1:]}
    if 'Items'      in lst: items |= {x.strip('- ') for x in lst.splitlines()[1:]}

  return name, doors, items


def part_1(data):

  prog = Interface(data)
  name, doors, it = parse_view(prog.command(''))

  reverse = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
  path    = ()
  graph   = {(): doors}
  items   = {(): it}
  names   = {(): name}

  # Explore and take all items
  while True:
    dest = {x for x in graph[path] if path+(x,) not in graph}
    if dest:
      path = path + (dest.pop(),)
      view = prog.command(path[-1])
      name, doors, it = parse_view(view)
      graph[path] = {x for x in doors if x != reverse[path[-1]]}
      items[path] = it
      names[path] = name
      for i in it:
        if i not in ('giant electromagnet','escape pod', 'infinite loop',
                     'photons', 'molten lava'):
          prog.command('take '+i)
      if name == 'Pressure-Sensitive Floor':
        path = path[:-1]
    elif path:
      prog.command(reverse[path[-1]])
      path = path[:-1]
    else:
      break

  # Drop items at Security Checkpoint
  for p in path:
    prog.command(reverse[p])
  for p in next(p for p, n in names.items() if n == 'Security Checkpoint'):
    prog.command(p)
  items_here = sorted(parse_view(prog.command('inv'))[2])
  for item in items_here:
    prog.command('drop ' + item)

  # Optimize weight
  go = next(p for p, n in names.items() if n == 'Pressure-Sensitive Floor')[-1]
  for i in range(2**len(items_here)):
    j = max(0, i - 1)
    for k in range(len(items_here)):
      if (i^j) & (2**k):
        if i & (2**k):
          prog.command('take ' + items_here[k])
        elif j & (2**k):
          prog.command('drop ' + items_here[k])
    view = prog.command(go)
    if 'Alert!' not in view:
      break

  return ''.join(filter(str.isnumeric, view))


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

