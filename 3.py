available_topping = ('mushrooms', 'olives', 'green peppers',
                     'pepperoni', 'pineapple', 'extra cheese')
requested_toppings = ['mushrooms', 'olives', 'extra cheese']

# 先检查是否存在无效配料
invalid = [t for t in requested_toppings if t not in available_topping]
if invalid:
    print(f"Sorry, we don't have {invalid[0]}.")
    print("Please choose your toppings again")
else:
    # 全部合法，再依次添加并收尾
    for topping in requested_toppings:
        print(f"Adding {topping}")
    print("\nFinish making your pizza!")