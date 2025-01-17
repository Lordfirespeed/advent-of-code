target = str(990941)
recipes = [3, 7]
elfa = 0
elfb = 1


def forwards_result():
    return "".join([str(i) for i in recipes[-1 * len(target):]])


def backwards_result():
    return "".join([str(i) for i in recipes[-1 * len(target) - 1:-1]])


while forwards_result() != target and backwards_result() != target:
    newrecipes = [int(i) for i in str(recipes[elfa] + recipes[elfb])]
    recipes += newrecipes
    elfa = (elfa + recipes[elfa] + 1) % len(recipes)
    elfb = (elfb + recipes[elfb] + 1) % len(recipes)

if forwards_result() == target:
    print(len(recipes) - len(target))
else:
    print(len(recipes) - len(target) - 1)
