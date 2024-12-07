import colorama
from colorama import Fore

colorama.init()
try:
  5/0
except Exception as e:
  print(Fore.RED+e)
