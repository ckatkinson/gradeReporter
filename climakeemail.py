import csv
import inquirer
import re


def qs(prompt, fields, mode):
    if mode == 'single':
        questions = [inquirer.List('answer',
                       message = prompt,
                       choices = fields,),]
        return questions
    elif mode == 'multiple':
        questions = [inquirer.Checkbox('answer',
                       message = prompt,
                       choices = fields,),]
        return questions



#Depending on your needs, you might need to modify the following. I've flagged
#each spot that mentions participation because I sometimes don't have a
#participation grade

class MakeEmail:

    def __init__(self, input_csv):
        with open(input_csv, 'r') as csv_file:
            self.csv_reader = csv.reader(csv_file)
            self.header = next(self.csv_reader)
            self.weights = next(self.csv_reader)
            self.csv_list = [row for row in self.csv_reader]
            self.studentscores = [dict(zip(self.header, x)) for x in
                                  self.csv_list]

            #try guessing the right fields
            rlast = re.compile("^(?i).*last.*")
            lastguess = list(filter(rlast.search, self.header))[0]

            rfirst = re.compile("^(?i).*first.*")
            firstguess = list(filter(rfirst.search, self.header))[0]

            remail = re.compile("^(?i).*email.*")
            emailguess = list(filter(remail.search, self.header))[0]

#Participation:
            rpart = re.compile("^(?i).*partic.*")
            partguess = list(filter(rpart.search, self.header))[0]

            roverall = re.compile("^(?i).*Overall.*")
            overallguess = list(filter(roverall.search, self.header))[0]

            rletter = re.compile("^(?i).*Letter.*")
            letterguess = list(filter(rletter.search, self.header))[0]
            ##^^those are our guesses. Below, we'll confirm that the guesses are
            #as expected.
            lookingood = input("""
            I've tried to guess some of the correct columns. How does this
            look?\n
            First name:     {}
            Last name:      {}
            Email:          {}
            Participation:  {}
            Overall:        {}
            Letter:         {}
            
            Type 'y' if it looks good and 'n' if it looks
            bad\n""".format(firstguess, lastguess, emailguess, partguess, overallguess, letterguess))
            #Participation in above line ^^^

            if lookingood == "y":
                self.first = firstguess
                self.last = lastguess
                self.email = emailguess
            #Participation below
                self.participation = partguess
                self.overall = overallguess
                self.lettergrade = letterguess
            #Participation below
                guessed = [firstguess, lastguess, emailguess, partguess,
                        overallguess, letterguess]
                remainder = self.header.copy()
                for x in guessed:
                    remainder.remove(x)
                self.scored = inquirer.prompt(qs('Select scored fields',
                    remainder, 'multiple'))['answer']
            else:
                print("""Well, I tried. Let's do it manually:""")
                self.last = inquirer.prompt(qs('Select last name', self.header,
                    'single'))['answer']
                self.first = inquirer.prompt(qs('Select first name', self.header,
                    'single'))['answer']
                self.email = inquirer.prompt(qs('Select email', self.header,
                    'single'))['answer']
            #Participation below
                self.participation = inquirer.prompt(qs('Select participation',
                    self.header, 'single'))['answer']
                self.overall = inquirer.prompt(qs('Select overall', self.header,
                    'single'))['answer']
                self.lettergrade = inquirer.prompt(qs('Select letter grade',
                    self.header, 'single'))['answer']
                self.scored = inquirer.prompt(qs('Select scored fields',
                    self.header, 'multiple'))['answer']
                for x in self.scored:
                    print(x)

            self.headerweights = dict(zip(self.header, self.weights))
            self.shortenedweights = [self.headerweights[x] for x in self.scored]

            self.scoredweights = dict([[x, self.headerweights[x]] for x in self.scored])

            self.weighttext = '\n'.join('{} is weighted as {} <br>'.format(*t) for t in
                    zip(self.scored, self.shortenedweights))

    def email_text_noindex(self, student, text, csv_file):
        overall = student[self.overall]
        letter = student[self.lettergrade]
            #Participation below
        partbank = student[self.participation]
        shrtstudentscores = [student[t] for t in self.scored]
        tabletitles = self.scored + ['Overall'] + ['Letter']
        tablescores = shrtstudentscores + [overall] + [letter]
        scoretable = '\n'.join('{}: {} <br>'.format(*t) for t in zip(tabletitles,
        tablescores))
        firstname = student[self.first]
        weights = self.weighttext
        with open(text) as txt:
            emailtext = txt.read()
            #Participation below
        return emailtext.format(firstname, weights, partbank,  scoretable)




