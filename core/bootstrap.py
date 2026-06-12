import sys, os

def os_check() -> None:
    if  sys.platform == "linux":
        print("ADD TO LOG - os type")
    else:
        pass

def shell_check() -> None:
    print(os.environ)

if __name__ == "__main__":
    print(sys.platform)
    print(os.environ.get("SHELL"))