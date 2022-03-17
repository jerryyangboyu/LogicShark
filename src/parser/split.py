# 此文件目的在于替换test8文件中的split库函数。
# Input：不管有多少个空格
# output：strings in lists
# example：INPUT: A ANDOR B NOTA ANDC))) OUTPUT:['A', 'AND', 'OR', 'B', 'NOT', 'A', 'AND', 'C', ')', ')', ')']
elems = input("please enter:")
generate_List = []
i = 0
print(len(elems))
for elem in elems:
    if (i <= len(elems) - 3):
        if elems[i:i + 3] == "NOT":  # 还得至少有三个空位
            generate_List.append("NOT")
            i += 3
        elif elems[i:i + 3] == "AND":  # 还得至少有三个空位
            generate_List.append("AND")
            i += 3
        elif elems[i:i + 2] == "OR":  # 还得至少有两个空位
            generate_List.append("OR")
            i += 2
        elif (elems[i] == "("):
            generate_List.append("(")
            i += 1
        elif (elems[i] == ")"):
            generate_List.append(elems[i])
            i += 1
        elif elems[i] == " ":
            i += 1
            pass
        elif elems[i].isalpha():
            (generate_List.append(elems[i]))
            i += 1

    elif (i <= len(elems) - 2):
        if elems[i:i + 2] == "OR":  # 还得至少有两个空位
            generate_List.append("OR")
            i += 2
        elif (elems[i] == "("):
            generate_List.append("(")
            i += 1
        elif (elems[i] == ")"):
            generate_List.append(elems[i])
            i += 1
        elif (elems[i] == " "):
            i += 1
            pass
        elif (elems[i].isalpha()):
            (generate_List.append(elems[i]))
            i += 1

    elif (i == len(elems)):
        pass

    else:
        if (elems[i] == "("):
            generate_List.append("(")
            i += 1
        elif (elems[i] == ")"):
            generate_List.append(elems[i])
            i += 1
        elif (elems[i] == " "):
            pass
            i += 1
        elif (elems[i].isalpha()):
            (generate_List.append(elems[i]))
            i += 1

    # print(generate_List," ",elem," ",i)
    print(generate_List)
