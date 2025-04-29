#!/usr/bin/python


def parse(inp):

  instructions = []

  for line in map(str.split, inp.readlines()):
    if line[-2] == 'new':
      instructions.append((0, None))
    elif line[-2] == 'cut':
      instructions.append((1, int(line[-1])))
    elif line[-2] == 'increment':
      instructions.append((2, int(line[-1])))
      

  return instructions


def get_new_position(instructions, position):

  for inst, val in instructions:
    if inst == 0:
      position = - position - 1
    if inst == 1:
      position = position - val
    if inst == 2:
      position = position * val

  return position


def get_old_position(instructions, position, n_cards):

  max_val = max(j for i,j in instructions if i==2) + 1

  for inst, val in instructions[::-1]:
    if inst == 0:
      position = - position - 1
    if inst == 1:
      position = position + val
    if inst == 2:
      position = pow(val, n_cards-2, n_cards) * position % n_cards

  return position % n_cards


def solve(func, func_r, position, n_cards, repeats):

  if repeats == 0: return position

  hist_r = []
  for i in range(100):
    hist_r.append(position)
    position = func_r(position)

  hist = []
  for i in range(100):
    hist.append(position)
    position = func(position)

  mult, add = map(n_cards.__rmod__, divmod(hist[-1], hist[-11]))

  func   = lambda pos: (pos * mult + add)
  func_r = lambda pos: pow(mult, n_cards-2, n_cards) * (pos-add) % n_cards

  return solve(func, func_r, hist_r[repeats%10] % n_cards, n_cards, repeats//10)


def part_1(data):

  return get_new_position(data, 2019) % 10007


def part_2(data):

  position = 2020
  n_cards  = 119315717514047
  repeats  = 101741582076661

  func_r   = lambda pos: get_old_position(data, pos, n_cards)
  func     = lambda pos: get_new_position(data, pos)

  return solve(func, func_r, position, n_cards, repeats)


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

