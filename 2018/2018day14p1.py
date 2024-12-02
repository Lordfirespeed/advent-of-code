improveafter = 990941
recipes = [3, 7]
elfa = 0
elfb = 1

while len(recipes) < improveafter + 10:
    newrecipes = [int(i) for i in str(recipes[elfa] + recipes[elfb])]
    recipes += newrecipes
    elfa = (elfa + recipes[elfa] + 1) % len(recipes)
    elfb = (elfb + recipes[elfb] + 1) % len(recipes)

print("".join([str(i) for i in recipes[-10:]]))
