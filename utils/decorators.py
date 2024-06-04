from colorama import Fore

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f'{Fore.RED}' + str(e) + f'{Fore.RESET}'
        except KeyError:
            return f'{Fore.RED}Enter user name{Fore.RESET}'
        except IndexError:
            return f'{Fore.RED}Please, provide all the required input {Fore.RESET}'
        except KeyboardInterrupt:
            print('\nBye-bye!')

    return inner
