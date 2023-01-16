


'''
.login :
    fileIO.login.add(["email", "password"]) -> add to the login table
    fileIO.login.remove(["email", "password"]) -> remove from the login table and delete all question registered if the password is correct
    fileIO.login.check(["email", "password"]) -> return true if the password is correct

.question : 
    fileIO.question.add("email", "question", ["answers"]) -> add the question to the question table
    fileIO.question.remove("email", "questionID") -> remove the question from the question table
    fileIO.question.update("email", "password", "question", ["answers"]) -> update the question in the question table
    fileIO.question.listByAccount("email") -> return all questions created by the account
    fileIO.question.listByTag("tag(s)") -> return all questions with the given tags
    fileIO.question.getById("questionID") -> return the question with the given ID
'''