#Group Members: Balint Hompot, Ludi Van Leeuwen, Mario Holubar, Prajakta Shouche

from QuestionParser import *
from QuestionAnswerer import *

import requests
import sys

###The system works as follows:
##reads an input -> finds groups of words of interest (regex) -> removes unimportant word types (POS) -> creates an ordered triple based on the patterns defined in specification -> Gets the ID for the words in the triple -> constructs a query using the IDs -> requests and prints answer for the quesry
##The system is very general, works on every domain, and new patterns can be added with only a definition in the specification, no need to change the code in ant way
##Example: pattern with Y's X is added besides X of Y, works perfectly

##############################################  define specification for the task here ###################################
spec1 = {
    'ignored_words':["is", "true", "false", "yes", "no", "list", "have"],
    'question_words':{'What': ["instance of", "subclass of"],
                      'Is': ["instance of", "subclass of"],
                      'Who':["instance of"],
                      'Where': ['continent'],
		      'When': ['point in time','start time','end time']
                      },
    'basic_question_formats':{"Object":[{'variable':'Object'},'Property', 'Result'],
                        "Property":['Object', {'variable':'Property'}, 'Result'],
                        "Result": ['Object', 'Property', {'variable':'Result'}]},
    'patterns':{'triples':{
                r"(.*) of ([^\\?]+)":['Property', 'Object', {'variable':'Result'}],
                r"(.*)'s ([^\\?]+)":['Object', 'Property', {'variable':'Result'}]
                ###Throughout the code I call the elements of a wikidata triple Object - Property - Result
                ###This dictionary defines what order of these entities corresponds to a pattern (key), so the parser will know how to put the query together
                ##regex stopword removal (kept for potential use later): (?:the|a|an)?\s*
                },
    },
    'deps':{"Object": ["pobj", "poss", "nsubj", "conj", "dobj", "npadvmod", "appos","attr", "nsubjpass"],                 ##we store here the possible deps (returned by spacy) for each element in a triple
            "Property" : ["attr", "nsubj", "acomp", "dobj","pcomp","pobj"],
            "Result": ["attr", "acomp", "advcl"]
            },
    'extended_deps':{"Object": ["dobj","compound"],                 ##The deps that should be considered when looking at the synonims and nounified words
                        "Property" : ["ROOT","acl","compound"],
                        "Result": ["pobj"]
                    },
    'true_false_list':{"starters":['is', 'has', 'does', 'was', 'do'],
                       "somewhereInText": ['true', 'false', 'yes', 'no']},
    'count_list':{"singles":["count","number"],          #single words
                "doubles":["how many", "how much"]},         #two word expressions
    'tags_of_interest': ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBS", "RBR", "VB", "VBD", "VBG", "VBP", "VBZ", "VBN"],
    'print':True,
    'common_IDs':{"highest": "P2044",
                  "high":"P2044",
                  "higher":"P2044",
                  "height":"P2044",
                  "longest": "P2043",
                  "long":"P2043",
                  "longer":"P2043",
                  "length":"P2043",
                  "member":"P150",
                  "county":"P150",
                  "state":"P150",
                  "language":"P37",            #language -> official language
                  "bigger":"P2046",
                  "big":"P2046",
                  "size":"P2046",

                  "depth":"P1589",
                  "deep":"P1589",

                  "eu":"Q458",
                  "us":"Q30",
                  "uk":"Q145",
                  "un":"Q1065",
                  "world":"Q2",

                  "is":"P31",
		          "eu":"Q458",
                  "us":"Q30",
                  "uk":"Q145",
                  "un":"Q1065",
                  "world":"Q2",
                  "administrative territory":"P150",
                  "territory":"P150",
                  "time period":"P2348",
                  "border":"P17",
                  "lowest":"P1589",
                  "low":"P1589",
                  "many people":"P1082",
                  "many inhabitants":"P1082",
                  "territorial entity":"P150",
                  "administrative territorial entity":"P150"
    }
}
###the specs are passed to the outer class as an argument, several versions can be defined here separately
##########################################################################################################################
import sys
import io


print("We assume you want to read questions from sysin. \n If you want to read questions from file, press 1\n If you want to read questions from std.in, press 2 (Exit by typing bye ) \n"
      " NOTE: WE ASSUME THE FIRST THREE CHARS NEED TO BE NEGLECTED \n")
x = input()

### NOTE: WE ASSUME THE FIRST THREE CHARS NEED TO BE NEGLECTED
answers = io.open(".\\answers.txt", "w", encoding='utf-8')
if x == "1":
    questions =open("test_questions.txt", "r")
    id = 1
    content = questions.readlines()
    for sentence in content:
        if len(sentence)>3:
            sentence = sentence[3:]
            print("question number " + str(id) + " is \n    ")
            print(sentence)
            ans = str(QuestionAnswerer(QuestionParser((sentence), Specification(spec1))).getAnswer())
            print("ANSWER IS " + ans)
            try:
                answers.write((str(id) + "   " + ans + "\n"))
            except:
                answers.write((str(id) + "     an error occurred\n"))
            id+=1
    answers.close()
    file = open('answers.txt', 'r')

else:
    id = 1
    sentence = ''
    while sentence != 'Bye':
        sentence = input("Enter a question:")
            print("question number " + str(id) + " is \n    ")
            print(sentence)
            ans = str(QuestionAnswerer(QuestionParser((sentence), Specification(spec1))).getAnswer())
            print("ANSWER IS " + ans)
            try:
                answers.write((str(id) + "   " + ans + "\n"))
            except:
                 answers.write((str(id) + "     an error occurred\n"))
            id += 1
    answers.close()
    file = open('answers.txt', 'r')