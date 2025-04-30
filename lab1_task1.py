def SumJewels():
    J = input()
    S = input()
    jewels = set(J)
    print (sum(1
               for stone in S
               if stone in jewels
               ))

SumJewels()