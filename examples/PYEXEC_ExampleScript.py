import colorama
from colorama import Fore

colorama.init()
try:
  if 5/0 == 0:
    print("What")
except Exception as e:
  print(f'{Fore.RED}Err:{e}')
