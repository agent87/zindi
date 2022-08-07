import itertools
import re
import pandas as pd
from string import punctuation
from spellchecker import SpellChecker

# showing full data without truncanations
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('data.csv')

english_stopwords = {"0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"}
kinyarwanda_stopwords = {
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'mu','ku','i',
    'na','nka',
    'mb', 'mf', 'mp', 'mv', 'nd', 'ng', 'ny', 'sh', 'nj', 'nk', 'ns', 'ts', 'nsh', 'nshy', 'nt', 'nz', 'bw', 'bg', 'cw', 'dw', 'fw', 'gw', 'hw', 'jw', 'kw', 'mw', 'nw', 'nyw', 'pfw', 'pw', 'rw', 'shw', 'shyw', 'sw', 'tsw', 'tw', 'vw', 'zw', 'by', 'cy', 'jy', 'my', 'nny', 'pfy', 'py', 'ry', 'sy', 'ty', 'vy', 'byw', 'myw', 'pfyw', 'ryw', 'vyw', 'mbw', 'mfw', 'mpw', 'mvw', 'ndw', 'ngw', 'njw', 'nkw', 'nshw', 'nshyw', 'nsw', 'ntw', 'nzw', 'mby', 'mpy', 'mvy', 'ncy', 'ndy', 'njy', 'nsy', 'nty', 'mbyw', 'mvyw', 'njyw',
    'aba', 'abo', 'aha', 'aho', 'ari', 'ati', 'aya', 'ayo', 'ba', 'baba', 'babo', 'bari', 'be', 'bo', 'bose','bw', 'bwa', 'bwo', 'by', 'bya', 'byo', 'cy', 'cya', 'cyo', 'hafi', 'ibi', 'ibyo', 'icyo', 'iki','imwe', 'iri', 'iyi', 'iyo', 'izi', 'izo', 'ka', 'ko', 'ku', 'kuri', 'kuva', 'kwa', 'maze', 'mu', 'muri','na', 'naho','nawe', 'ngo', 'ni', 'niba', 'nk', 'nka', 'no', 'nta', 'nuko', 'rero', 'rw', 'rwa', 'rwo', 'ry','rya','ubu', 'ubwo', 'uko', 'undi', 'uri', 'uwo', 'uyu', 'wa', 'wari', 'we', 'wo', 'ya', 'yabo', 'yari', 'ye','yo', 'yose', 'za', 'zo'}


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
    