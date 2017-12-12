def sum (a):
  if a<=1:
    return a
  else:
    return a + sum(a-1)
    
    
print(sum(int(input())))

input()