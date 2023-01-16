import os.path

if os.path.exists('.\static\save.txt'):
    print("init save file")
    with open('.\static\save.txt', 'w') as out:
        print("\n\n\n==========\n\n\n", file=out)

""" 

def load:


def save: """