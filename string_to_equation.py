from terms.variable import Variable


def string_to_equation(string):
    variable_list = []

    string = string.replace('^', '**')
    string = string.replace(' ', '')
    i = 0
    while i < len(string):
        char_at_i = string[i]
        if char_at_i not in ['+', '-', '*', '/', ')', '('] and char_at_i.isdigit() == False:
            i, string = replace_char_with_variable(i, string)
            variable_list.append(Variable(char_at_i))
        else:
            i += 1
    return eval(string), tuple(variable_list)


def replace_char_with_variable(index, string):
    replacement_string = 'Variable("' + string[index] + '")'

    first_half = string[:index]
    second_half = string[index+1:]

    returned_string = first_half + replacement_string + second_half
    index_after_replacement = index + len(replacement_string)
    return index_after_replacement, returned_string




















