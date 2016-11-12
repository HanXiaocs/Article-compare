#name: Han Xiao
#xh1994@bu.edu
#Partner: Wanjing Ma
#Partner's email: wanjingm@bu.edu

import math
def split(txt):
    s = ''
    lst = []
    for i in txt:
        if i not in '.?!':
            s += i
        else:
            lst += [str(s)]
            s = ''
            
    new_lst = []
    
    for n in lst:
        if n[0] is ' ':
            n = n[1:]
            new_lst += [str(n)]
        else:
            new_lst += [str(n)]             
    return new_lst
            
            

def clean_text(txt):
    """returns a list containing the words in txt after it has been “cleaned”"""
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace('?', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('!', '')
    txt = txt.replace('-', '')
    txt = txt.replace('(', '')
    txt = txt.replace(')', '')
    txt = txt.lower()
    txt = txt.split()
    return txt

def stem(word):
    """return the stem of word."""
    if word[-3:] in ['ing', 'cal', 'ful', 'ary', 'ish']:
        if len(word) > 6:
            if word[-4] == word[-5]:
                word = word[:-4]
            else:
                word = word[:-3]
    elif word[-2:] == 'er':
        if len(word) > 5:
            if word[-3] == word[-4]:
                word = word[:-3]
            else:
                word = word[:-2]
    elif word[-1:] == 's':
        if len(word) > 4:
            if word[-3:] == 'ies':
                word = word[:-2]
            else:
                word = word[:-1]
    elif word[-3:] == 'est':
        if len(word) > 6:
            if word[-4] == word[-5]:
                word = word[:-4]
            else:
                word = word[:-3]
    elif word[-2:] == 'ed':
        if len(word) > 5:
            if word[-3] == word[-4]:
                word = word[:-3]
            else:
                word = word[:-2]
    elif word[-2:] == 'ly':
        if len(word) > 5:
            if word[-3] == word[-4]:
                word = word[:-3]
            else:
                word = word[:-2]
    elif word[-1:] == 'y':
        word = word[:-1] + 'i'
    elif word[-1:] == 'e':
        word = word[:-1]
    elif word[-4:] in ['tion', 'able', 'ment']:
        if len(word) > 5:
            word = word[:-4]
    return word

def compare_dictionaries(d1, d2):
    """return their log similarity score. """
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    for i in d2:
        if i in d1:
            score += d2[i] * math.log(d1[i] / total)
        else:
            score += d2[i] * math.log(0.5 / total)
    return score

        



    
class TextModel:
    def __init__(self, model_name):
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.first_word = {}
       

    def __str__(self):
        """ returns a string that includes the name of the model as
        well as the sizes of the dictionaries for each feature of the text."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of first words: ' + str(len(self.first_word))
        return s

    def __repr__(self):
        """evaluating it directly"""
        return str(self)

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        sentences = split(s)
        for i in sentences:
            sentence_split = i.split()
            len_sentence = len(sentence_split)
            if len_sentence not in self.sentence_lengths:
                self.sentence_lengths[len_sentence] = 1
            else:
                self.sentence_lengths[len_sentence] += 1
        
        for i in sentences:
            word_split = i.split()
            if word_split[0] not in self.first_word:
                self.first_word[word_split[0]] = 1
            else:
                self.first_word[word_split[0]] += 1    
            

        # Add code to clean the text and split it into a list of words.
        s = clean_text(s)
        # *Hint:* Call one of your other methods!
        
        # Code for updating the words dictionary.
        for w in s:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1

        # Add code to update other feature dictionaries.
        for w in s:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
        for w in s:
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
                

    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        f_str = f.read()
        self.add_string(f_str)
        f.close()

    #part2
    def save_model(self):
        """saves the TextModel object self by writing its
        various feature dictionaries to files"""
        f1 = open(self.name + '_' + 'words' + '.txt', 'w')      # Open file for writing.
        f1.write(str(self.words))              # Writes the dictionary to the file.
        f1.close()                    # Close the file.
        f2 = open(self.name + '_' + 'word_lengths' + '.txt', 'w')
        f2.write(str(self.word_lengths))
        f2.close()
        f3 = open(self.name + '_' + 'self.stems' + '.txt', 'w')
        f3.write(str(self.stems))
        f3.close()
        f4 = open(self.name + '_' + 'self.sentence_lengths' + '.txt', 'w')
        f4.write(str(self.sentence_lengths))
        f4.close()
        f5 = open(self.name + '_' + 'self.first_word' + '.txt', 'w')
        f5.write(str(self.first_word))
        f5.close()

    def read_model(self):
        """reads the stored dictionaries for the called
        TextModel object from their files and assigns them
        to the attributes of the called TextModel"""
        f1 = open(self.name + '_' + 'words' + '.txt', 'r')    # Open for reading.
        d1_str = f1.read()           # Read in a string that represents a dict.
        f1.close()

        self.words = dict(eval(d1_str))      # Convert the string to a dictionary.

        f2 = open(self.name + '_' + 'word_lengths' + '.txt', 'r')    # Open for reading.
        d2_str = f2.read()           # Read in a string that represents a dict.
        f2.close()

        self.word_lengths = dict(eval(d2_str))      # Convert the string to a dictionary.

        f3 = open(self.name + '_' + 'self.stems' + '.txt', 'r')    # Open for reading.
        d3_str = f3.read()           # Read in a string that represents a dict.
        f3.close()

        self.stems = dict(eval(d3_str))      # Convert the string to a dictionary.

        f4 = open(self.name + '_' + 'self.sentence_lengths' + '.txt', 'r')    # Open for reading.
        d4_str = f4.read()           # Read in a string that represents a dict.
        f4.close()

        f5 = open(self.name + '_' + 'self.first_word' + '.txt', 'r')    # Open for reading.
        d5_str = f5.read()           # Read in a string that represents a dict.
        f5.close()

        self.first_word = dict(eval(d5_str))      # Convert the string to a dictionary.

    def similarity_scores(self, other):
        """returns a list of log similarity scores measuring the similarity of self and other """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        first_word_score = compare_dictionaries(other.first_word, self.first_word)
        score_lst = [word_score, word_lengths_score, stems_score, sentence_lengths_score, first_word_score]
        return score_lst

    def classify(self, source1, source2):
        """compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2)
        and determines which of these other TextModels is the more likely source of the called TextModel"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for source1 : ', scores1)
        print('scores for source2 : ', scores2)
        sim1 = 0
        sim2 = 0
        if scores1[0] > scores2[0]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[1] > scores2[1]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[2] > scores2[2]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[3] > scores2[3]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[4] > scores2[4]:
            sim1 += 1
        else:
            sim2 += 1
        if sim1 > sim2:
            print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)


def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ your docstring goes here """
    source1 = TextModel('JKR')
    source1.add_file('JK.txt')

    source2 = TextModel('Eshakespeare')
    source2.add_file('Shakespearem.txt')

    new1 = TextModel('wr098')
    new1.add_file('WR98.txt')
    new1.classify(source1, source2)

        


        



    

  
