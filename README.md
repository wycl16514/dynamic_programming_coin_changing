在动态规划问题中，有一个很常见的问题就是最少硬币兑换。假设当前有面额为1，2，5元的硬币，然后给你一定额度，要求你将额度兑换成等值硬币，并要求兑换硬币的数量要最少。例如给定的额度为9元，那么兑换的方法有[5, 1, 1, 1, 1]， [5,2,2], [2,2,2,1]，很显然第二种兑换方法最好。

如果你了解前面描述的动态规划方法，那么这个问题的处理不难。这个问题有意思在于，它有相应的变种问题和解法值得一说，我们先看看该问题除了动态规划之外的解法。这个问题还能用BFS，也就是广度有限搜索来处理，方法如下：
![请添加图片描述](https://img-blog.csdnimg.cn/30e450cf5dac41c9b159f38f4066fa0c.png)
如上图所示，我们把问题转换为一个图的遍历问题。最顶层是要兑换的面额，然后根据不同硬币数值进行兑换后得到第二层，例如当前硬币数值为[1,2,5]，面额为9，那么分别兑换硬币1，2，5后所得数额分别为8，7，4，接下来分别针对第二层3个节点进行相应操作。注意我们这里要使用广度优先搜索，也就是我们按照层次来遍历节点，首先处理第一层，然后处理第二层，以此类推，当遇到第一个值为0的节点时，我们就找到了硬币数最少的兑换方案，例如在上面例子中，第三层出现了0节点，因此得到问题的解，那么从根节点到当前节点对应的数值就是所兑换的硬币数值。同时需要注意的是，并发每个节点都能再延伸出下层节点，例如第二层的节点4因为不能再使用面值为5的硬币兑换，因此它不能产生对应分支。

我们看看代码实现：
```
class ChoiceNode:
    def __init__(self, coins, total_value, this_coin):
        self.coins = coins
        self.total_value = total_value # 当前还能兑换的数额

        if total_value < 0:
            raise ValueError("total value < 0")

        if (this_coin in coins) is False:
            raise ValueError("coin value invalid")

        self.__current_selected_coins = [this_coin]

    def __repr__(self):
        return print(f"value:{self.total_value}, changes:{self.__current_selected_coins}")

    def __str__(self):
        return print(f"value:{self.total_value}, changes:{self.__current_selected_coins}")

    def making_changes(self, notify_change_complete):
        if self.total_value == 0:
            notify_change_complete(self.__current_selected_coins)  # 面值全部转换成了硬币，通知相应结果
            return []

        coins_selected = []
        for coin in self.coins:  #创建选择分支
            if coin <= self.total_value:
               # print(f"value:{self.total_value} coin:{coin}")
                selected_coin = ChoiceNode(self.coins, self.total_value - coin, coin)
                selected_coin.__current_selected_coins += self.__current_selected_coins # 记录下当前所有选择的硬币
                coins_selected.append(selected_coin)

        return coins_selected


class CoinChanging:
    def __init__(self, coins, total_value):
        if total_value <= 0:
            raise ValueError("changing value <= 0")

        if 1 not in coins: #必须要有面值为1的硬币，要不然可能无法实现有效兑换
            raise ValueError("coins not contain value 1")

        self.coins = coins
        self.total_value = total_value
        self.uncomplete_choice_nodes = []
        self.__make_initial_choice()
        self.best_choice = None # 记录当前最好的方案
        self.keep_chaning = True

    def __make_initial_choice(self):
        for coin in self.coins:
            if coin < self.total_value:
                choice = ChoiceNode(self.coins, self.total_value - coin, coin)
                self.uncomplete_choice_nodes.append(choice)

    def coin_changing(self):
        while len(self.uncomplete_choice_nodes) != 0 and self.keep_chaning is True:
            choice = self.uncomplete_choice_nodes.pop(0)
            self.uncomplete_choice_nodes += choice.making_changes(self.notify_complete)

        print(f"the best coin changing solution is : {self.best_choice}")

    def  notify_complete(self, solution):
        self.best_choice = solution
        self.keep_chaning = False


solution = CoinChanging([1, 2, 5], 33)
solution.coin_changing()
```
上面代码运行后结果如下：
```
[5, 5, 5, 5, 5, 5, 2, 1]
```

这个问题有一个变种，处理起来也不容易，那就是给定具体面额，要求算法给出总共有多少种不重复的兑换方案。例如给定数额3，存在的方案有，[1, 2], [2, 1], [1,1,1],但[1,2]和[2,1]是同一种方案，因此两者只能算做一种。

我们看一个具体实例，假设要兑换的面额有6，那么对应的方案有：
1,1,1,1,1,1
1,1,1,1,2
1,5
2,2,2
从实例上看，所有方案的集合有一些特点：某一些方案的集合包含了硬币1，某些方案的集合不包含1，某些方案的集合不包含硬币1，2，依次类推，我们看看代码实现：
```
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
```
上面代码运行后结果如下：
```
36 solutions
```
变种问题其实用BFS来解决效果更好，相应的办法就是，到第二层时，最左边的节点及其之后的子节点都可以分出3个分支，第二层中间节点在延伸出子节点时，它只考虑硬币[2，5]产生的分钟，第二层最后一个节点在延伸出子节点时只考虑硬币5产生的分支，如此来看解决硬币兑换问题，其实使用BFS方法效果更好.
