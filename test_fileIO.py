import fileIO
fileIO.login.create("e", "f")
print(fileIO.login.check("e", "f"))
fileIO.question.newQuestion("e", "aaaaaaaa", ['a', 'b', 'c'], ["a", "b", "c"])
fileIO.question.newQuestion("e", "aaaaaaaa", ['d', 'e', 'f'], ["d", "e", "f"])

for item in fileIO.question.listByAccount("e"):
    print(fileIO.question.read(item))

fileIO.login.remove("e")