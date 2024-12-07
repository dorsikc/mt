import colorama
from colorama import Fore

colorama.init()
try:
  print(5/0)
except Exception as e:
  print(Fore.RED+e)
