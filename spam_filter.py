# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 23:31:53 2015

@author: wcramblit
"""

import os
from collections import Counter
import re
from compiler.ast import flatten
import string

'''
train_dict returns a dictionary where k = a single word and v = probability of that word appearing in a text file in the directory, path_to_file
'''

def train_dict(path_to_file):
    punct = set(string.punctuation)
    file_count = 0
    email_list = []
    for f in os.listdir(path_to_file): #iterate through directory
        file_count += 1
        doc_list = []
        with open(str(path_to_file) + str(f)) as current_file: #open file
            qlist = [item.split() for item in current_file] #break into lists
            qlist = flatten(qlist) # correct for newline
            qlist = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in qlist] #punctuation 
            qlist = filter(None, qlist) #remove blank space entry
            for word in qlist: #iterate through words in list
                if word.lower() not in doc_list: #check if word is already in file
                    doc_list.append(word.lower()) #add word to file's list of words
                    email_list.append(word.lower()) #add word to list
    email_dict = Counter(email_list) #create dictionary with words and counts
    for k, v in email_dict.iteritems(): #iterate list and get probs for each term
        email_dict[k] = float(v/float(file_count))
    return email_dict

'''
email_prob takes a text file and determines the probability that it is spam based on trained dictionaries ham_probs and spam_probs
'''

def email_prob(path_to_text_file, ham_probs, spam_probs):    
    prob_list = [] #list of probabilities that will be factored
    doc_list = [] #will be used to create list of words in doc
    with open(str(path_to_text_file)) as current_file: #open text file
        qlist = [item.split() for item in current_file] #break into lists
        qlist = flatten(qlist) # correct for newline
        qlist = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in qlist] #punctuation 
        qlist = filter(None, qlist) #remove blank space entry
        for word in qlist: #iterate through words in list
            if word.lower() not in doc_list: #check if word is already in file
                doc_list.append(word.lower()) #add word to file's list of words
    #now doc_list is a list of words in the document
    #establish our key values for bayes calculation
    prob_ham = float(len(ham_probs)/float((len(ham_probs) + len(spam_probs))))
    prob_spam = 1-prob_ham
    spam_bayes = []
    for word in doc_list: #iterate through terms in our email
        prob_word_in_spam = 0
        for k,v in spam_probs.iteritems(): #iterate through our spam probs
            if k == word and word != 'subject':
                prob_word_in_spam += float(spam_probs[k]) #assign values
        for k,v in ham_probs.iteritems(): #iterate through our ham probs
            if k == word and word != 'subject':
                prob_word_in_ham = float(ham_probs[k]) #assign values
        if prob_word_in_spam > 0.0:
            prob_word = float((prob_word_in_spam * prob_spam) + (prob_word_in_ham * prob_ham))
            prob_spam_given_word = float((prob_word_in_spam * prob_spam) / (prob_word))
            spam_bayes.append(float((prob_spam_given_word * math.log(prob_word/(1-prob_word))) + math.log(1-prob_word)))
    
    log_prob_email_is_spam = 0
    for val in spam_bayes:
        log_prob_email_is_spam += val
    return math.exp(log_prob_email_is_spam)

'''
function calls to test each and complete our analysis
'''    
    

ham_path = 'emails/ham/' #pass the directory containing ham messages
spam_path = 'emails/spam/' #pass the directory containing spam messages
ham_probs = train_dict(ham_path)
spam_probs = train_dict(spam_path)

#call email_prob to define probability that an email is spam
text_file = 'emails/spamtest.txt' #pass a test email file
email_prob(text_file, ham_probs, spam_probs)