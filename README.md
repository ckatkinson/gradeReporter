# gradeReporter
Sends grade reports to students.

Requires python3, [prompt_toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) and 
[python-inquirer](https://github.com/magmax/python-inquirer).

I wrote this code to send grade reports to students. It's fairly 
specialized to my syllabi and my way of recording grades, but is 
easily modifiable. In particular, the grades must be in a csv. The first row must be the field 
names. The second row must be the weighting that is being used to
compute grades. The third row should be where the student grades begin.

Run gradeReporter.py to get started. Try using the file example.csv when prompted along with emailtext.txt. These example files will not send any emails, so you can see how it works as setup safely.

See the code and modify to your needs.
