def ask_true_or_false(msg):
    ''' True か False を選択させる '''
    while True:
        print(msg, end='')
        selection = prompt_inputting_decimal()
        if selection == 1:
            return True
        elif selection == 2:
            return False
        else:
            print('please input 1 - 2 ! >д<;')


def ask_number(msg, limit):
    ''' limit以下の数値を選択させる '''
    while True:
        print(msg, end='')
        number = prompt_inputting_decimal()
        if number > limit:
            print('[ALERT] 0から{}までの値を入力してください'.format(limit))
        else:
            return number


def select_from_dict(dictionary, menumsg='選択して下さい'):
    menu = '[interface] {}'.format(menumsg)
    dict_len = len(dictionary)
    for i, (key, val) in enumerate(dictionary.items()):
        menu = '{menu} [{key}]:{val},'.format(menu=menu, key=key, val=val)
    menu = menu[0:-1] + ': '

    while True:
        print(menu, end='')
        selection = input()
        if selection in dictionary:
            return dictionary[selection]
        else:
            print('[interface] please input {} - {} ! >д<;'.format(dictionary.keys()[0], dictionary.keys()[-1]))


def prompt_inputting_decimal():
    '''
    整数を入力させ、int型にして返す
    Parameters
    ----------
    -
    Returns
    -------
    int: decimal
    '''
    while True:
        selection = input()
        if selection.isdecimal():
            return int(selection)
        else:
            print('Please, input the positive value (integer) ! \nINPUT AGAIN: ', end='')
