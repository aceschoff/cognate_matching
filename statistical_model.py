"""
Statistical model for decipherment of languages via character-set alignment. 
"""

# Imports
import nltk     # pip install nltk
import pandas as pd
import numpy as np

from nltk.translate import IBMModel2, AlignedSent, Alignment    # pip install


class StatisticalCharacterAlignment():
    def __init__(self, filepath: str = None, source = [], target = [], source_chars: str = '', target_chars: str = ''):
        super.__init__(StatisticalCharacterAlignment, self)

        # can either pass in string names of the languages and a filepath or the language data already formatted as lists of words
        if type(source) == str:
            self.source, self.target = self.read_file(filepath, source, target)
        else:
            self.source = source
            self.target = target

        # making these passed in for now but could include the function to actually find them
        self.source_chars = source_chars
        self.target_chars = target_chars

        # Create corpus
        self.corpus = self.create_corpus(self.source, self.target)
        # instantiate Statistical Model -- IBM Model 2
        self.mister_ibm = IBMModel2(self.corpus, 20)


    def read_file(self, filepath: str, source, target):
        """
        !!!!!!!!!! preprocessing has to happen before reading !!!!!!!!!!!
        read in and process data to be formatted like ['a', 'l', 't',...] per lang
        """
        df = pd.read_csv(filepath)

        lang_x = df[source].values.tolist()
        lang_y = df[target].values.tolist()

        return lang_x, lang_y
    
    def create_corpus(self, source, target):
        """
        format the data intoa list of NLTK AlignedSent types to be used when instantiating model
        """
        #lengths need to be the same so we don't have ny empty pairs
        assert len(source) == len(target)

        corpus = []
        for i in range(len(source)):
            corpus.append(AlignedSent(list(source[i]), list(target[i])))
        return corpus
    
    def find_alignment(self):
        """
        Only need source chars as input because we will pick up best pairing with target chars as we go
        should probably make this a dictionary instead if you can
        """
        alignment = []
        for char in self.source_chars:
            prev = -1
            for key, value in self.mister_ibm.translation_table[char].items():
                if value > prev:
                    best = key
                    best_val = value
                    prev = value
            alignment.append((char, best, best_val))
        # Currently only really works as a printout -- need to modify to be able to automate building a usable alignment, rather than just finding it
        print(alignment) 
        return alignment