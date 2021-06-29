from re import search
#Prompt user for input, compare to items in tuple, if input doesn't match
#string in compare tuple, error and prompt again. Additionally user can type
#help and the optional usr_help will print if provided
def matching(prompt, compare, usr_help=None, err_msg='Incorrect input, try again!'):
    while True:
        try:
            x = input(prompt)
            if x in compare:
                return x
            elif usr_help and x == 'help':
                print(usr_help)
                continue
            else: raise Exception
        except: print(err_msg)

#Prompt user for input, compare it to regex, if input doesn't pass regex, retry
#Also allows user to ask for help if usr_help provided
def specific(prompt, regex, usr_help=None, err_msg='Incorrect input, try again!'):
    while True:
        try:
            x = input(prompt)
            if search(regex, x):
                return x
            elif usr_help and x == 'help':
                print(usr_help)
                continue
            else: raise Exception
        except: print(err_msg)

#Prompt user for a numerical int, retry input if incorrect input, allows user to
#ask for help if usr_help provided, returns int as str if return_str true
def number_int(prompt, usr_help=None, err_msg='Incorrect input, try again!', return_str=False):
    while True:
        try:
            x = input(prompt)
            if usr_help and x == 'help':
                print(usr_help)
                continue
            elif return_str and x.isdigit():
                return x
            else: return int(x)
        except: print(err_msg)

#Prompt user for a numerical float, retry input if incorrect input, allows user to
#ask for help if usr_help provided, returns float as str if return_str true
def number_float(prompt, usr_help=None, err_msg='Incorrect input, try again!', return_str=False):
    while True:
        try:
            x = input(prompt)
            if usr_help and x == 'help':
                print(usr_help)
                continue
            else: x = float(x)
            if return_str: return str(x)
            else: return x
        except: print(err_msg)