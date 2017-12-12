def primes_less_than(limit:int):
    primes = []
    nums = range(1,limit)
    i = 0
    while i < limit-1:
        is_prime = True
        for prime in primes[1:]:
            if nums[i] % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(nums[i])
        i += 1
    return primes

print(primes_less_than(10000))