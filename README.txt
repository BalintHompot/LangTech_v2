README:
This program works by moving to the project directory and running
"python3 main.py test_questions.txt" in the commandline, where 
"test_questions.txt" is the file containing the questions that you 
want to test (with three chars before each question, for space+id+tab,
and a newline after each questions).

In the program, you have 2 options: either you run from the commandline,
where you type in each question (with three chars again), or you run
the program from a pre-written file called "test_questions.txt", which
contains all the test questions. You can run from file by pressing "1",
and press any other key to run from commandline.

3 characters are removed as the test questions on nestor have the format 
space-ID-tab-question, although the description in the slides does not mention space.

It is necessary to install some modules. This can be done with pip3, or
inside the PyCharm IDE. These modules are:
requests, sys, spacy, nltk, termcolor and word2number.
