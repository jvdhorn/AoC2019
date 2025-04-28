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


def navigate(chart, pos, drc):

  end    = chart.index(10) + 1
  turns  = {-end: (-1, 1), end: (1, -1), -1: (end, -end), 1: (-end, end)}
  run    = 0
  result = []

  while True:
    if chart[pos + drc] == 35:
      run += 1
      pos += drc
    else:
      if run: result.append(str(run)); run = 0
      turn_l, turn_r = turns[drc]
      if chart[pos + turn_l] == 35:
        result.append('L')
        drc = turn_l
      elif chart[pos + turn_r] == 35:
        result.append('R')
        drc = turn_r
      else:
        break

  return result


def segment(route, depth=0):

  if not route:
    return [[]]
  elif depth > 2:
    return [None]

  result = []
  possible_chunks = [sub[:i+1] for sub in route for i in range(len(sub))]
  for chunk in possible_chunks:
    size      = len(chunk)
    remaining = []
    for sub in route:
      cleared = ' '.join(sub).replace(' '.join(chunk), '').split('  ')
      for subsub in cleared:
        new_sub = subsub.split()
        if new_sub: remaining.append(new_sub)
    segmented_remaining = segment(remaining, depth+1)
    if None not in segmented_remaining:
      for option in segmented_remaining:
        result.append([chunk]+option)

  return result


def get_routine(route, segments):

  route    = ','.join(route)
  segments = [','.join(segment) for segment in segments]
  result   = ''

  while route:
    for i, segment in enumerate(segments):
      if route.startswith(segment):
        route   = route.replace(segment, '', 1).strip(',')
        result += '%c,'%(i+65)

  return result.strip(',')


def part_1(data):

  prog   = intcode(data)
  prog.run()
  end    = prog.stdout.index(10) + 1
  lines  = list(zip(*end*[iter(prog.stdout)]))

  inter  = {(i,j+1) for i, row in enumerate(lines) for j, _ in enumerate(row)
            if row[j:j+3].count(35) == 3}
  lines  = list(zip(*lines))
  inter &= {(j+1,i) for i, row in enumerate(lines) for j, _ in enumerate(row)
            if row[j:j+3].count(35) == 3}

  return sum(a*b for a,b in inter)


def part_2(data):

  prog  = intcode(data)
  prog.run()
  chart = prog.stdout[:]
  end   = chart.index(10) + 1
  chart = chart[:-1] + [46] * (end-1)
  drcs  = {94:-end, 86:end, 60:-1, 62:1}

  pos   = next(i for i, val in enumerate(chart) if val in drcs)
  drc   = drcs[chart[pos]]
  route = navigate(chart, pos, drc)
  sgmts = segment([route])
  sgmts = list({tuple(map(tuple, s)) for s in sgmts
           if all(len(','.join(chunk))<=20 for chunk in s)})

  for option in sgmts:
    routine = get_routine(route, option)
    if len(routine) <= 20:
      segments = option
      break
  
  prog = intcode((2,) + data[1:])
  prog.stdin += list(map(ord, routine + '\n'))
  for s in segments:
    prog.stdin += list(map(ord, ','.join(s) + '\n'))
  prog.stdin += list(map(ord, 'n\n'))
  prog.run()

  return prog.stdout[-1]


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

