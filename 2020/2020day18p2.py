from math import prod

with open(r"Input\2020day18.txt") as inputfile:
    inputlines = [line.strip() for line in inputfile.readlines()]


def eval_expr(expr):
    brackets = []
    replaced_expr = expr
    for index, char in list(enumerate(expr))[::-1]:
        if char == ")":
            brackets.append(index)
        if char == "(":
            end_bracket = brackets.pop(-1)
            if len(brackets) == 0:
                replaced_expr = replaced_expr[:index] + str(eval_expr(expr[index+1:end_bracket])) + replaced_expr[end_bracket+1:]

    operands_and_operators = replaced_expr.split(" ")
    operands = [int(number) for index, number in enumerate(operands_and_operators) if index % 2 == 0]
    operators = [operator for index, operator in enumerate(operands_and_operators) if index % 2 == 1]

    for index, operator in list(enumerate(operators))[::-1]:
        if operator == "+":
            operands[index] += operands.pop(index+1)

    return prod(operands)


results = [eval_expr(expr) for expr in inputlines]

print(f"Sum of results to math problems: {sum(results)}")
