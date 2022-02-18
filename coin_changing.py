'''
[1,2,5]
7: 1...1; 2,5
'''
coins_map = {} # 用来记录问题的解
coins = [1, 2, 5]

def coin_making(amount, coins, index): # 生成的方案不包含index前面对应的硬币
    if index >= len(coins) or amount < 0:
        return None

    if amount == 0:  #兑换的数值为0则无需任何方案
        return [ [] ]

    if (amount, index) in coins_map: # 查看是否已经有了答案
        return coins_map[(amount, index)]

    solutions = []
    for i in range(index, len(coins)): # 从index 之后的硬币中寻求兑换方案
        if coins[i] > amount: # 如果当前硬币数值已经大于面额，那么不存在可行的兑换方案
            coins_map[(amount, i)] = None
            break

        sub_solutions = coin_making(amount - coins[i], coins, i) # 递归的处理规模更小的子问题
        if sub_solutions is not None: # 如果子问题存在解决方案，那么结合起来得到整个问题的解决方案
            for sub_solution in sub_solutions:
                solution = [coins[i]]
                solution += sub_solution
                solutions.append(solution)

    coins_map[(amount, index)] = solutions

    return coins_map[(amount, index)]

amount = 23
coin_making(amount, coins, 0)
count = 0
for i in range(len(coins)):
  if (amount, i) in coins_map:
      if coins_map[(amount, i)] is not None:
          #print(coins_map[(amount, i)])
          count += len(coins_map[(amount, i)])

print(f"{count} solutions")


