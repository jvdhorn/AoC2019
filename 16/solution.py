#!/usr/bin/python


def parse(inp):

  return tuple(map(int, inp.read().strip()))


def get_smallest_prime_factors(lim, cache = dict()):

  factors = cache.get(lim)

  if factors is None:
    numbers = range(2, lim+1)
    factors = dict.fromkeys(numbers)

    for i in numbers:
      if not factors[i]:
        factors[i] = i
        j          = i * i
        while j <= lim:
          factors[j] = i
          j         += i

    cache[lim] = factors

  return factors


def get_primes(lim, cache = dict()):

  primes = cache.get(lim)

  if primes is None:
    primes     = sorted(set(get_smallest_prime_factors(lim - 1).values()))
    cache[lim] = primes

  return primes


def group(it, n):

  l = len(it)
  x = 0
  i = 1
  t = 0
  while x < l:
    part = sum(it[x:x+n])
    yield part
    x += n
    i *= 1j
    if   i ==  1: t += part
    elif i == -1: t -= part

  yield abs(t) % 10


def fft(inp):

  inp     = [0] + list(inp)
  lim     = len(inp)
  primes  = get_primes(lim-1)
  nprim   = len(primes)
  *res, s = group(inp, 2)
  stack   = [[2,0,res,s]]
  done    = {1: abs(sum(inp[1::4]) - sum(inp[3::4])) % 10}

  while stack:
    n, i, sums, s = stack[-1]
    nxt           = n * primes[i]
    if nxt < lim and nxt not in done:
      *res, s = group(sums, primes[i])
      stack.append([nxt, i, res, s])
    else:
      stack.pop()
      done[n] = s
      if i+2 <= nprim:
        nxt = n // primes[i] * primes[i+1]
        if nxt < lim and nxt not in done:
          sums    = stack[-1][2] if stack else inp
          *res, s = group(sums, primes[i+1])
          stack.append([nxt, i+1, res, s])

  return [i for _, i in sorted(done.items())]


def fft2(inp):

  size   = len(inp)
  result = [0] * size

  for i in range((size+1)//2):
    prev_first = prev_second = total = 0
    for j in range(size):
      first  = 2 * i + j * (2 * i + 1)
      if first >= size: break
      second = min(first + j + 1, size)
      if prev_second <= first:
        total = sum(inp[first:second])
      else:
        total -= sum(inp[prev_first:first])
        if second > prev_second:
          total += sum(inp[prev_second:second])
      prev_first, prev_second = first, second
      result[j] += -total if i%2 else total

  return [abs(i) % 10 for i in result]


def part_1(data):

  for _ in range(100):
    data = fft(data)

  return ''.join(map(str, data[:8]))


def part_2(data):

  offset = int(''.join(map(str, data[:7])))
  data   = data * 10000

  for _ in range(100):
    data = fft2(data)

  return ''.join(map(str, data[offset:offset+8]))


if __name__ == '__main__':

  with open(0) as inp:
    data = parse(inp)

  sol1 = part_1(data)
  print(sol1)

  sol2 = part_2(data)
  print(sol2)

