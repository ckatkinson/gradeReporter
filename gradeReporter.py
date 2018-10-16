#!/usr/local/bin/python3
'''
gradeReporter sends grade reports to a list of students specified by a csv. See
example.csv for the format needed. In particular, the first row should name the
fields that you're reporting on. The second row should have the weights for the
various scored fields. Student rows should start in the third row. 

This file sets up the email server, asks for email and password (it's gmail
specific, but I'd guess that it's easily modifiable. It then calls
climakeemail.MakeEmail to put together the email.
'''
import smtplib
import getpass
import os
from subprocess import call
#Need relatively recent prompt_toolkit for WordCompleter to be included
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import climakeemail


#Put together the email headers
def headers(sender, subject, recipient):
    headers=["From: " + sender, "Subject: " + subject, "To: " + recipient, "MIME-Version: 1.0","Content-Type: text/html"]
    return "\r\n".join(headers)



def spamEmails(csv_file, text, sender, password, subject):
    #get email stuff ready:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(sender, password)

    #get info from the csv_file. This also extracts the fields and entries
    #needed to write the email using the MakeEmail class:
    data = climakeemail.MakeEmail(csv_file)
    scores = data.studentscores

    #Look at a test email. Can proceed to look at further test emails or
    #enter editor to edit the template if it looks bad.
    ready = ""
    stu = 0
    test_email = data.email_text_noindex(scores[stu], text, csv_file)

    #don't leave this loop unless the user types 'I am ready'
    while ready != 'I am ready':
        os.system('clear')
        print("""--------------------\n""")
        print(test_email)
        print("""--------------------\n""")
        ready = input("""
        Does that email look ok? If so, type 'I am ready'. If
        you want to see another email, type 'a'. If you want to edit
        the email template, type 'edit'. Type anything else if
        things are bad and we'll abort:\n""")
        #if the user inputs 'a', load up another email:
        if ready ==  'a':
            stu+=1
            test_email = data.email_text_noindex(scores[stu], text, csv_file)
            print(test_email)
        #if the user inputs 'edit', fire up the editor and let them make
        #changes
        elif ready == 'edit':
            EDITOR = os.environ.get('EDITOR', 'vim') #get the editor (if
                                                     #$EDITOR not set, get vim
            call([EDITOR, text])
            test_email = data.email_text_noindex(scores[stu], text, csv_file)
        #If they type anything else, abort. This will send emails, so it's
        #set up to be excessively careful!
        elif ready != 'a' and ready !='I am ready':
            print("Report aborted!")
            return -1
        print("\n\n\n")

    #iterate through sheet, building and sending one email after another.
    for student in scores:
        emailtext = data.email_text_noindex(student, text, csv_file)
        if '@' not in student[data.email]:
            print('No email listed for {} {}'.format(student[data.first],
                    student[data.last]))
            pass
        else:
            server.sendmail(sender, student[data.email], headers(sender,
                subject, student[data.email]) + "\r\n\r\n" + emailtext)
            print('Sending email to {} {} at {}'.format(student[data.first],
                    student[data.last], student[data.email]))
    server.close()


#This is setting up the completers for autocompleting (using prompt_toolkit). If
#you replace that obviously fake email address below with your email, then it'll
#autocomplete
lcom = ['email@fakeemailplace.com']
for root, dirs, files in os.walk("."):
    for filename in files:
        lcom.append(filename)

commonentries = WordCompleter(lcom)

#Those are some example courses that I use frequently. Change to suit your needs
courses = WordCompleter(['1101', '1102', '2101', '3111'])


def main():
    #ask user for the necessary info and call the spam function.
    sender = prompt('Type gmail address:  ', completer=commonentries)
    password = getpass.getpass('Type gmail password:  ')
    course = prompt('What is the class number:  ', completer=courses)
    subject = 'Math {} grade report'.format(course)
    csvfile = prompt('csv filename?  ', completer=commonentries)
    text = prompt('Email text?  ', completer=commonentries)
    spamEmails(csvfile, text, sender, password, subject)
if __name__ == "__main__":
    main()


