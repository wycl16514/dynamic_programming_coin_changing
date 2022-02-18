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







