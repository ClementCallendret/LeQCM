import fileIO
fileIO.login.create("e", "f")
print(fileIO.login.check("e", "f"))
fileIO.question.newQuestion("e", "aaaaaaaa", ['a', 'b', 'c'], ["a", "b", "c"])
fileIO.question.newQuestion("e", "aaaaaaaa", ['d', 'e', 'f'], ["d", "e", "f"])
print(str(fileIO.question.read("0")))
print(str(fileIO.question.read("1")))
fileIO.question.remove('1')