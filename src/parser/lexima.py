# input:[(A AND B) AND C]
# output: Tree
# 这是该进后的生成逆波兰式代码，test8.py中的还未以此代码更新
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
# 运算符元组
OPERATORS = ('AND', 'OR', 'NOT', '(', ')')
# 优先级
PRIORITY = dict([('AND', 1), ('OR', 1), ('NOT', 2)])


# 依次压栈并追加到后缀表达式，直到遇到左括号为止
def pop_left_bracket(postfix, operators):
    while operators:
        operator = operators.pop()
        # 抵消前面的左括号
        if operator == '(':
            break
        # 如果是其他符号那么就继续放在运算符中
        else:
            postfix.append(operator)


# 输入的是符号，比较优先级并进行相应操作
def compare_and_pop(i, postfix, operators):
    if len(operators) == 0:
        operators.append(i)
        return

    while operators:
        operator = operators.pop()
        if operator == '(':
            operators += ['(', i]
            return
        # 栈越上面优先级越高，越先覆盖
        # 遇到一个优先级更高的，这是唯一一种不先用的情况，所以不可能堆栈超过两个
        elif PRIORITY[i] > PRIORITY[operator]:
            operators += [operator, i]
            return
        # 遇到一个优先级小的，赶紧先用了，因为它要先用，优先级小代表作用范围就小
        elif PRIORITY[i] < PRIORITY[operator]:
            print("done")
            print(operators)
            while len(operators) != 0 and PRIORITY[i] < PRIORITY[operator]:
                postfix.append(operator)
                operator = operators.pop()
            # 底下已经没有东西
            # if (len(operators)==0):
            #     operators.append(i)
            # 底下还有个AND或者OR
            if PRIORITY[i] == PRIORITY[operator]:
                print("postfix:", postfix)
                print("operator:", operator)
                print("operators:", operators)
                postfix.append(operator)
                operators.append(i)
            return
        # AND 与 OR 同时出现,向前前置,他也要先用
        elif PRIORITY[i] == PRIORITY[operator]:
            if i == operator and operator == "NOT":
                operators += [operator, i]
            else:
                postfix.append(operator)
                operators.append(i)
            return


# 弹出所有剩余的运算符，追加到后缀表达式，完成最后的逆波兰式
def pop_rest(postfix, operators):
    while operators:
        postfix.append(operators.pop())


# 判断是否为英文字母输入
def is_input(input):
    if len(input) == 1:
        return True
    elif len(input) != 1:
        return False


# 将中缀表达式转换为后缀表达式
def infix_to_postfix(infix):
    infix = infix.split()
    postfix = []
    operators = []
    # 待处理的list
    print(infix)

    for i in infix:
        # 如果是字母那么就加入到postfix列表中
        if is_input(i) and (i != "(") and (i != ")"):
            postfix.append(i)
        # 如果是运算符就加入到 operators 列表中
        elif i in OPERATORS:
            # 左括号处理
            if i == '(':
                operators.append(i)
            # 右括号处理
            elif i == ')':
                pop_left_bracket(postfix, operators)
            # 普通运算符处理
            else:
                compare_and_pop(i, postfix, operators)

    pop_rest(postfix, operators)

    return postfix


# 字符流 -> 逆波兰式
def main():
    infix = input('please input equation:')

    postfix = infix_to_postfix(infix)  # 转换成逆波兰式

    postfix = ' '.join(postfix)

    print(postfix)

    return postfix


if __name__ == '__main__':
    main()

# 本片改进点完全在此法分析器中
# 改进点：1.要求没有空格也可以输入 自动机 (完成，但并非用自动机方法)
# 2. 没有括号可以自动加括号 A AND NOT B OR C
# 3. 括号不对齐可以自动判断 ((((((
# 4. 恶心输入也可以输出 NOT NOT NOT NOT A
