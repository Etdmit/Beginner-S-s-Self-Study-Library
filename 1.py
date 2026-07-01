import random


# 定义一个函数
def guess_game():
    # random是引入的随机数函数，后面的randint很好理解，“rand”+“int”,得到一个整数
    n = random.randint(1, 100)
    print("Try to guess a number:")
    # Ture保证while为真，始终能运行
    while True:
        m = int(input())
        if m < n:
            print("Too low!Guess again:")
        elif m > n:
            print("Too high!Guess again:")
        else:
            print("Guess right!Do you want to play again?")
            # input()输入，strip()去掉输入两边可能出现的空白符，lower()将输入全部转化为小数
            again = input().strip().lower()
            if again == "yes":
                guess_game()
            else:
                print("Thank you for playing!")
            break


guess_game()
