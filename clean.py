import itertools
import re
import pandas as pd
from string import punctuation
from spellchecker import SpellChecker
from lib.stopwords import *

# showing full data without truncanations
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('data.csv')

english_stopwords = english_stopwords
kinyarwanda_stopwords = kinyarwanda_stopwords

patterns = {
    "email":'[0-9a-zA-Z\._-]+@[0-9a-zA-Z\._-]+\.[\s]?[a-z]+[\.]?[\s]?[\s]?[edu|com|comgt|uk|ch]*',
    "urls":r'\bhttp[s]?[:,\.\w]*[\s/\\]+[\s/\\]+[\w\s]+\w[:\.]+[\s\w]+[-\w]+[\s\.]?[\.]?[\s]?[\w{3}]*',
    "hashtags": '[#][a-z_0-9]+',
    "phone": '\(\d{3}\)-\d{3}-\d{4}|\d{10}',
    "tags":"<[a-zA-Z]*>[\s]*\w*[\s]*</[a-zA-Z]*>"
}

class RuleBased:
    def __init__(self, df):
        self.df = df
    
    def print_dataset(self, columns=[]):
        if len(columns)>0:
            return self.df[columns]
        return self.df
    
    def occurences(self, temp):
        major_ = len(list(itertools.chain(*temp)))
        print('Number of Occurences',major_)
        return major_
    
    def remove_pattern(self, pattern, column, replacement='', surrounding=True, remove=False, display=True):
        found_words = list()
        temp_column = list()
        origin = pattern
        surrounding_pattern = '[\w+\s+]*'
        
        # add surrounding words to the special character
        if surrounding:
            pattern = surrounding_pattern+pattern+surrounding_pattern
        for item in self.df[column]:
            temp = re.findall(pattern, item)
            if remove:
                temp_column.append(re.sub(origin, replacement, item))
            if(len(temp)>0):
                found_words.append(temp)
                if display:
                    print(temp)
                
        if remove:
            self.df[column] = temp_column
        self.occurences(found_words)
        return self.df
    
    def remove_known_patterns(self, pattern, column, display=False, remove=False, replacement=""):
        temp_column = []
        if(pattern in list(patterns.keys())):
            pattern = patterns[pattern]

            for sentence in self.df[column]:
                temp = re.findall(pattern, sentence)
                if display and temp:
                    print(temp)
                    print(sentence)
                if remove:
                    sentence = re.sub(pattern, replacement, sentence)
                    
                if display and temp:
                    print(sentence)
                temp_column.append(sentence)
            
            self.df[column] = temp_column
            return self.df
        else:
            return "try patterns, "+list(patterns.keys())
    
    def remove_punctuations(self, column):
        temp_column = list()
        for sentence in self.df[column]:
            no_punct_string = re.sub(r'[^\w\s]', '', sentence)
            temp_column.append(no_punct_string)
        self.df[column]=temp_column
        return self.df
        
    def remove_special_characters(self, column):
        temp_column = list()
        for sentence in self.df[column]:
            no_special_string = re.sub('[@_!#$%^&*()<>?/\|}{~:]','',sentence)
            temp_column.append(no_special_string)
        self.df[column] = temp_column
        return self.df
    
    def normalize(self, column):
        temp_column = []
        for sentence in self.df[column]:
            normalized_text = sentence.lower()
            temp_column.append(normalized_text)
        self.df[column] = temp_column
        return self.df
    
    def remove_stopwords(self, column):
        if column=='English':
            stopwords = english_stopwords
        elif column=='Kinyarwanda':
            stopwords = kinyarwanda_stopwords
            
        temp_column = []
        for sentence in self.df[column]:
            text = " ".join([word for word in str(sentence).split() if word not in stopwords])
            temp_column.append(text)
        self.df[column] = temp_column
        return self.df
    
    def remove_numbers(self, column):
        temp_column = []
        for sentence in self.df[column]:
            no_numbers = re.sub('[0-9]+','',sentence)
            temp_column.append(no_numbers)
        self.df[column] = temp_column
        return self.df
        
    def spell_checker(self, column):
        if column!='English':
            return 'Language is not available'
        temp_column = []
        
        spell = Spellchecker()
        
        def checking(sentence):
            ls = np.asarray(list(sentence.split(" ")))
            misspelled = spell.unknown(ls)
            for i in range(len(ls)):
                for incorrect in misspelled:
                    if ls[i]==incorrect:
                        ls[i] = spell.correction(incorrect)
            return " ".join(str(word) for word in ls)
                
        for sentence in numpy.asarray(self.df[column]):
            temp_column.append(checking(sentence))
            
        self.df[column] = temp_column
        return self.df
        
    def save(self,name='cleaned_data_for_en_kin_trans'):
        name_ = name+'.csv'
        print('File Saved...')
        self.df.to_csv(name_)
        
obj = RuleBased(df)

obj.remove_known_patterns('email', column='English', remove=True, replacement="")
obj.remove_known_patterns('urls', column='English', remove=True, replacement="")
obj.remove_known_patterns('hashtags', column='English', remove=True, replacement="")
obj.remove_known_patterns('phone', column='English', remove=True, replacement="")
obj.remove_known_patterns('tags', column='English', remove=True, replacement="")

obj.remove_known_patterns('email', column='Kinyarwanda', remove=True, replacement="")
obj.remove_known_patterns('urls', column='Kinyarwanda', remove=True, replacement="")
obj.remove_known_patterns('hashtags', column='Kinyarwanda', remove=True, replacement="")
obj.remove_known_patterns('phone', column='Kinyarwanda', remove=True, replacement="")
obj.remove_known_patterns('tags', column='Kinyarwanda', remove=True, replacement="")

obj.remove_punctuations(column='English')
obj.remove_punctuations(column='Kinyarwanda')

obj.remove_numbers(column='English')
obj.remove_numbers(column='Kinyarwanda')

obj.normalize(column='English')
obj.normalize(column='Kinyarwanda')

obj.remove_stopwords(column='English')
obj.remove_stopwords(column='Kinyarwanda')

obj.remove_special_characters(column='English')
obj.remove_special_characters(column='Kinyarwanda')

# obj.spell_checker(column='English')
obj.save()
obj.df.iloc[110:150]
    