#from cli import parser
from core import bootstrap

def main() -> None:
   base_check: str = bootstrap.base_checks()
   if  base_check.startswith('ERR_'):
      #call the cli to show the errors
      print(base_check)
   
   print(base_check)

if __name__ == "__main__":
   main() 