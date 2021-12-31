import random

class Question(object):
    fragetext = None
    level = None
    antwortmoeglichkeit = None
    antwort = None

    def __init__(self, fragetext, level, antwortmoeglichkeit, antwort):
        if not 0 <= level <= 4:
            raise ValueError("Level has no good value.")
        self.level = level
        self.fragetext = fragetext
        self.antwortmoeglichkeit = antwortmoeglichkeit
        self.antwort = antwort

    def __str__(self):
        return str(self.level) + " " + self.fragetext + " " + self.antwortmoeglichkeit.__str__() + " " + str(self.antwort)

class Module(object):
    def read_questions(fName):
        questions = []
        file = open(fName, 'r')
        for line in file:
            line = line.replace("\n", "")
            if line[0].isnumeric():
                question = line.split("\t")
                answers = [question[2], question[3], question[4], question[5]]
                random.shuffle(answers)
                end_question = Question(question[1], int(question[0]), answers, answers.index(question[2]))
                questions.append(end_question)
        return questions

    def get_rand_question(level, questions):
        questions_level = []
        for i in questions:
            if i.level == level:
                questions_level.append(i)
        return random.choice(questions_level)

   



