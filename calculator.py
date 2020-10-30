# Calculator that follows PEMDAS, it still needs more error messages and the ability to multiply cases like '(2)(2)'.

# Checks if input has '=' at the end, and also if it has numeric values and operators only.
def check_input(inp):
    if inp[-1] != '=':
        print('Error: Input must end with "=".')
        return exit()
    for i in inp:
        if i != '+' and i != '-' and i != '/' and i != '*' and i != '=' and i != '.' and i != '(' and i != ')' and i != '^' \
                and not i.isdigit():
            print('Error: Input must only be numeric value or arithemtic operator.')
            return exit()

# Takes the input list, which includes the numbers and operands as seperate items, and the index of the items which is 0 by
# default, adds or subtracts the numbers that surround the operator, and spits out the same list but with the operations done.


def add_sub(input_list, i=0):
    result = []
    # Returns input list with finished operations once it finds '='.
    if input_list[i] == '=':
        return input_list
    # Adds surounding opperands, turns list into the result of that operation plus the remaining items of the previous list,
    # function calls itself, returns input_list
    elif input_list[i] == '+':
        result.append(float(input_list[i - 1]) + float(input_list[i + 1]))
        input_list = result + input_list[i + 2:]
        input_list = add_sub(input_list)
        return input_list
    # Same as above comment
    elif input_list[i] == '-':
        result.append(float(input_list[i - 1]) - float(input_list[i + 1]))
        input_list = result + input_list[i + 2:]
        input_list = add_sub(input_list)
        return input_list
    # Iterates through the lists items if the are not opperands.
    else:
        input_list = add_sub(input_list, i + 1)
        return input_list

# Takes the input list, which includes the numbers and operands as seperate items, and the index of the items which is 0 by
# default, multiplies or divides the numbers that surround the operator, and spits out the same list but with the operations
# done.


def mult_div(input_list, i=0):
    result = []
    # Returns input list with finished operations once it finds '='.
    if input_list[i] == '=':
        return input_list
    # Multiplies surrounding opperands, *turns list into the the items before the scope of the operations, the result of the
    # operation, and the items after the scope of the operation*, function calls itself, new list is returned.
    # **You might have noticed this is different from the add_sub function in the add_sub function adds or subs
    # the list's items and creates a new list whose first item is the result of the operations and this whole thing repeats.
    # This was done to account for PEMDAS. Add_sub function doesnt have to account for pemdas as this function will return
    # the results of mult/div as single items in the list, leaving only addition and subraction which is dealth with by
    # add_sub after.
    elif input_list[i] == '*':
        result.append(float(input_list[i - 1]) * float(input_list[i + 1]))
        input_list = input_list[:i - 1] + result + input_list[i + 2:]
        input_list = mult_div(input_list)
        return input_list
    # Same as comment from above.
    elif input_list[i] == '/':
        result.append(float(input_list[i - 1]) / float(input_list[i + 1]))
        input_list = input_list[:i - 1] + result + input_list[i + 2:]
        input_list = mult_div(input_list)
        return input_list
    # Iterates through the lists items if the are not opperands.
    else:
        input_list = mult_div(input_list, i + 1)
        return input_list

# The reasoning behind this function is similar to the mult_div one except with exponents, while not mandated by the
# program (yet?) , it is wise to use parentheses after the power symbol.


def exponent(input_list, i=0):
    result = []
    if input_list[i] == '=':
        return input_list
    elif input_list[i] == '^':
        result.append(float(input_list[i - 1]) ** float(input_list[i + 1]))
        input_list = input_list[:i - 1] + result + input_list[i + 2:]
        input_list = exponent(input_list)
        return input_list
    else:
        input_list = exponent(input_list, i + 1)
        return input_list

# This function creates a list of the opperands and operators in order by analizing the characters of the inputted string.
# It also deals with parentheses in the input.


def list_func(inp, input_list, index=0, old_index=0):
    # Checks if input characters is '=', in which case it appends the previous opperand and '=' to the list. It then removes
    # empty items and returns the list to be worked on by the operation functions.
    if inp[index] == '=':
        input_list.append(inp[old_index:index])
        input_list.append('=')
        return clean_list(input_list)
    # Checks if input character is opperator, in which case it adds the previous opperand and then the operator to the list,
    # and the reruns the function but this time it checks the next character.
    elif not inp[index].isdigit() and inp[index] != '.' and inp[index] != '(' and inp[index] != ')':
        input_list.append(inp[old_index:index])
        input_list.append(inp[index])
        return list_func(inp, input_list, index + 1, index + 1)
    # Negative numbers need to be surrounded by parentheses in order for them to be read by the program. If the character in
    # the input is a parentheses followed by a negative sign, neg_num returns a negative number. It also returns the index of
    # the ')' that way when list_func is called, it does not iterate through the negative number again but on the characters
    # after the closed parentheses.
    elif inp[index] == '(' and inp[index + 1] == '-':
        num = neg_num(inp, index + 2)[0]
        input_list.append(num)
        new_index = neg_num(inp, index + 2)[1] + 1
        return list_func(inp, input_list, new_index, new_index)
    # If list_func finds a '(' in the input not followed by a '-', it will add '(' to the input_list, but then replace it with
    # another value. A new input_list will be made from scratch whithin the list_func which is called as seen below, and it'll
    # include the operators and operands within the parentheses of the inputted string. That input_list will be worked on by
    # the operation algorithms and that result will be returned by list_func and will be the value that will replace the '('
    # mentioned earlier. list_func will be called again to return the index of ')' which will be used as the continuation
    # point for list_func so that it does not iterate over the characters within the parentheses again.
    elif inp[index] == '(':
        input_list.append('(')
        input_list[-1] = list_func(inp, [], index + 1, index + 1)[0]
        new_index = list_func(inp, [], index + 1, index + 1)[1]
        return list_func(inp, input_list, new_index, new_index)
    # Once the program runs into ')' it will add the final operand and operator within the new input_list and the operation
    # algorithms will work on it to compute the result of the input list and will be returned by the function and assigned
    # as the final item of the previous input_list. The function will also return the index of ')' + 1 so that the previous
    # input list does not iterate over the same operands and operators within the parenthese.
    elif inp[index] == ')':
        input_list.append(inp[old_index:index])
        input_list.append('=')
        # Operation algorithms are arranged according to PEMDAS
        return (add_sub(mult_div(exponent(clean_list(input_list))))[0], index + 1)
    # Function iterates over input characters
    else:
        return list_func(inp, input_list, index + 1, old_index)

# Right after list_func was done the parentheses, the next item after the appended result would be nothing and then
# it be the remaining operands and operators. Unfortunately, these empty items would mess with the operation functions so this
# function was needed to remove empty items.


def clean_list(input_list):
    for i in (input_list):
        if i == '':
            input_list.remove(i)
    return input_list

# Returns negative number enclosed within parentheses and the index of ')' so that list_func analyses input after ')'


def neg_num(inp, index, num=''):
    for i in inp[index:]:
        if i != ')':
            num += i
            index += 1
        else:
            break
    num = 0 - int(num)
    return (num, index)


# Program prompts user for input
inp = str(input())

check_input(inp)

input_list = []

# Operation algorithms are arranged according to PEMDAS
result = add_sub(mult_div(exponent(list_func(inp, input_list))))[0]

print(result)
