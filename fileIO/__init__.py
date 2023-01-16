import fileIO.login as login
import fileIO.question as question

from pathlib import Path
import os
__all__ = ['login', 'question', 'common']

if not(Path("./static/login.txt").is_file()):
    print("init save file")
    with open('./static/login.txt', 'w') as out:
        print("", file=out)

if not(Path("./static/question").is_dir()):
    print("init reppo")
    os.mkdir('./static/question')

if not(Path("./static/question.txt").is_file()):
    with open('./static/question.txt', 'w') as out:
        print("", file=out)