import itertools
import re
import pandas as pd
from string import punctuation
from spellchecker import SpellChecker
from stopwords import *

# showing full data without truncanations
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('data.csv')

english = english_stopwords
kinyarwanda = kinyarwanda_stopwords

patterns = {
    "email":'[0-9a-zA-Z\._-]+@[0-9a-zA-Z\._-]+\.[\s]?[a-z]+[\.]?[\s]?[\s]?[edu|com|comgt|uk|ch]*',
    "urls":r'\bhttp[s]?[:,\.\w]*[\s/\\]+[\s/\\]+[\w\s]+\w[:\.]+[\s\w]+[-\w]+[\s\.]?[\.]?[\s]?[\w{3}]*',
    "hashtags": '[#][a-z_0-9]+',
    "phone": '\(\d{3}\)-\d{3}-\d{4}|\d{10}',
    "tags":"<[a-zA-Z]*>[\s]*\w*[\s]*</[a-zA-Z]*>",
    "numbers":"[0-9]+",
    "characters":"[@_!#$%^&*()<>?/\|}{~:;-]",
    "punctuations":r'[^\w\s]',
    "pattern": "pattern"
}


class TextCleaning:
    def __init__(self, df):
        self.df = df
    
    def dataset(self):
        return self.df
    
    def pattern(self, pattern_name, show=False, regex=""):
        if(pattern_name in list(patterns.keys())):
            pattern_name = patterns[pattern_name]
            
            if pattern_name == "pattern":
                if regex == '':
                    return 'Please Enter a Pattern'
                pattern_name = regex
                
            for column in self.df:
                temp_column = []
                for sentence in self.df[column]:
                    temp = re.findall(pattern_name, sentence)
                    sentence = re.sub(pattern_name, "", sentence)

                    if show and temp:
                        print(sentence)
                    temp_column.append(sentence)

                self.df[column] = temp_column
            return self.df
        else:
            return "/!\ Choose among these patterns "+list(patterns.keys())
            
    def normalize(self):
        for column in self.df:
            temp = []
            for sentence in self.df[column]:
                temp.append(sentence.lower())
            self.df[column] = temp
        return self.df
    
    def stopwords(self, column):
        if column=='English':
            stopwords = english
        elif column=='Kinyarwanda':
            stopwords = kinyarwanda
        else:
            return "We don't have the stopwords for this language."
            
        temp_column = []
        for sentence in self.df[column]:
            text = " ".join([word for word in str(sentence).split() if word not in stopwords])
            temp_column.append(text)
        self.df[column] = temp_column
        return self.df
        
    def spell_checker(self, column):
        if column!='English':
            return 'Language not available'
        temp_column = []
        
        spell = SpellChecker()
        
        def checking(sentence):
            ls = list(sentence.split(" "))
            misspelled = spell.unknown(ls)
            for i in range(len(ls)):
                for incorrect in misspelled:
                    if ls[i]==incorrect:
                        ls[i] = spell.correction(incorrect)
            print(" ".join(str(word) for word in ls))
            return " ".join(str(word) for word in ls)
                
        for sentence in self.df[column]:
            temp_column.append(checking(sentence))
            
        self.df[column] = temp_column
        return self.df
        
    def save(self,file='cleaned_data_for_translation'):
        print('File Saved As '+file)
        self.df.to_csv(file+'.csv')

        
obj = TextCleaning(df)

obj.pattern('email')
obj.pattern('urls')
obj.pattern('hashtags')
obj.pattern('phone')
obj.pattern('tags')
obj.pattern('numbers')
obj.pattern('punctuations')

obj.normalize()

obj.stopwords(column='English')
obj.stopwords(column='Kinyarwanda')

obj.pattern('characters')

# obj.spell_checker(column='English')
obj.save()
obj.df.iloc[110:150]
    