import fileIO
fileIO.login.create("e", "f")
print(fileIO.login.check("e", "f"))
fileIO.question.newQuestion("e", "aaaaaaaa", ['a', 'b', 'c'], ["a", "b", "c"])
fileIO.question.newQuestion("e", "aaaaaaaa", ['d', 'e', 'f'], ["d", "e", "f"])
fileIO.question.newQuestion("e", "aaaaaaaa", ['1', '2', '3'], ["a", "b", "c"])

fileIO.question.update("1",'aaa',['1','2','3'])
for item in fileIO.question.listByAccount("e"):
    print(fileIO.question.read(item))
for item in fileIO.question.listByTag("a"):
    print(fileIO.question.read(item))
for item in fileIO.question.listByTags(['a','b']):
    print(fileIO.question.read(item))

fileIO.login.remove("e")