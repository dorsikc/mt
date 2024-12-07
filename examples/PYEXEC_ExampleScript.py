import colorama
from colorama import Fore

colorama.init()
try:
  print(str(5/0))
except Exception as e:
  print(Fore.RED+e)
