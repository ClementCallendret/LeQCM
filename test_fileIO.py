import fileIO
fileIO.login.create("e", "f")
print(fileIO.login.check("e", "f"))
fileIO.question.newQuestion("e", "title1", "aaaaaaaa", ['a', 'b', 'c'], ["a", "b", "c"], ["a"])
fileIO.question.newQuestion("e", "title2", "aaaaaaaa", ['d', 'e', 'f'], ["d", "e", "f"], ["d", "e"])
fileIO.question.newQuestion("e", "title3", "aaaaaaaa", ['1', '2', '3'], ["a", "b", "c"], ['1'])

fileIO.question.update("2", "new title",'aaa',['d','e','f'], ["d", "e", "f"], ["d"])
for item in fileIO.question.listByAccount("e"):
    print(fileIO.question.read(item))
for item in fileIO.question.listByTag("a"):
    print(fileIO.question.read(item))
for item in fileIO.question.listByTags(['a','b']):
    print(fileIO.question.read(item))
print(fileIO.question.listByTags(['d','e','f']))
print(fileIO.question.listByAccountAndTags('e', ['d','e','f']))
print(fileIO.question.isCorrect("1", ["1"]))
fileIO.login.remove("e")
fileIO.login.changePassword("test", "test1")