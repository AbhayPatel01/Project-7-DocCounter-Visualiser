# Idea 1. 
    # Minimalistic, module use. 

    # Programming Paradigm: OOP, Procedural; Hybrid. 
    # Progrmming Structure: main -> and callbacks, creation of objects 
    # Programming Style: pep8 like.  
    # Program Improvement/To Do: 
        # Flexible output. (with output, argument: for data: dataframe,json,csv,html,xml,etc.. for bar plot: dashboard, styling, etc..) 
        # Algo DS, etc..

# Base Case Works -> Other cases, visuals etc. not tested.

import argparse
import re
import pprint 
import pandas as pd 
import seaborn as sns 
import subprocess


parser = argparse.ArgumentParser(
                prog='DocCounter',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='''     Document Counter\n---------------------------------------------------------------- \n - Gets One or More Documents and Creates Data Visualisations. 
                            ''', 
                allow_abbrev=True)
parser.add_argument('filename',nargs='+',help='Input File(s) To Perform Count Operations On')
parser.add_argument('-w','-words',action='store_true',help='Count Words')
parser.add_argument('-l','-letters',action='store_true',help='Count Letters')
parser.add_argument('-p','-punctuation',action='store_true',help='Count Punctuation')
parser.add_argument('-c','-characters',action='store_true',help='Count Characters')
parser.add_argument('-o','-open',action='store_true',help='Open Bar Chart Visualisations For Count(s).')

arguments = parser.parse_args()
# print(arguments)

class Document:
    __DOCUMENT_COUNT = 0

    def __init__(self, document_name):
        Document.__DOCUMENT_COUNT += 1 
        self._document_name = document_name

    @staticmethod
    def get_document_count(cls): 
        return cls.__DOCUMENT_COUNT

    def punctuation(self) -> dict: 
        ''' Punctuation Count '''
        punctuation = {}
        with open(self._document_name,'r') as doc_handler: 
            for line in doc_handler: 
                line = re.sub('[a-zA-Z \n]*','',line)
                for x in line:
                    if x in punctuation: 
                        punctuation[x] += 1
                    else: 
                        punctuation[x] = 1

        return punctuation

    def letter_count(self) -> dict:
        ''' Letter Count '''
        letters = {}
        with open(self._document_name,'r') as doc_handler: 
            for line in doc_handler:  
                line = re.sub(r"(\w*)[\n !\"#\$%&\\'\(\)\*\+,-\.\/:;<=>\?@\[\]\^_`{\|}~]*(\w*)",r"\1\2", line).lower()
                for x in line: 
                    if x in letters : 
                        letters[x] += 1
                    else: 
                        letters[x] = 1
        return letters
     
    def word_count(self) -> dict:
        ''' Word Count'''
        words = {}
        with open(self._document_name,'r') as doc_handler: 
            for line in doc_handler:  
                line = re.sub(r"(\w*)[!\"#\$%&\\'\(\)\*\+,-\.\/:;<=>\?@\[\]\^_`{\|}~]*(\w*)",r"\1\2", line).lower()
                for x in line.split(): 
                    if x in words : 
                        words[x] += 1
                    else: 
                        words[x] = 1
        return words
    
    def character(self) -> dict:
        ''' Character Count, Lower Case & Upper Case & Special Characters e.g. \n. '''
        characters = {}
        with open(self._document_name,'r') as doc_handler: 
            for line in doc_handler: 
                for x in line: 
                    if x in characters: 
                        characters[x] += 1
                    else: 
                        characters[x] = 1
        return characters

    def get_name(self): 
        return '_'.join(self._document_name.split())


pp = pprint.PrettyPrinter()

def visualise_common(count: dict,semantic: str, document: Document): 
    count_len = len(count.keys())
    count_remainder = count_len % 10  
    if count_remainder > 5: 
        count_len += 10 - count_remainder
    else: 
        count_len -=  count_remainder
    height = count_len // 5 
    width = height
    sns.set(rc={'figure.figsize':(width, height)})


    pp.pprint(count)
    df = pd.DataFrame({k:[v] for k,v in count.items()}).T.reset_index().rename(columns={'index':semantic,0:'count'}) 
    fig = sns.barplot(data=df,x='count',y= semantic)
    fig.set_title(semantic + ' Count Bar Plot')

    figure_name = document.get_name() + semantic + '_count' + '_bar_plot' 
    extensions = ['.png','.jpeg']
    for extension in extensions: 
        fig.get_figure().savefig(figure_name + extension)
    print('File Saved in Current Directory As:', figure_name, 'as jpeg and png')


def visual_formatter(func,semantic,style_char,document): 
    print( 5 * style_char + ' '+ semantic.title() + ' ' + 'Count' + ' ' + 5 * style_char)
    visualise_common(func(),semantic,document)
 
def visualise(): 

   for file_num,  file in enumerate(arguments.filename): 
        document = Document(file)
        print()
        print( '\033[94m' + 'File ' + str(file_num) + '\033[0m' + ' ' + '\033[92m' +  file + ':' + '\033[0m')
        if arguments.w: 
            visual_formatter(document.word_count, 'word','~-',document)
        
        if arguments.l: 
            visual_formatter(document.letter_count, 'letter','=-',document)

        if arguments.p: 
            visual_formatter(document.punctuation, 'punctuation','-#',document)

        if arguments.c: 
            visual_formatter(document.character, 'character',"/\\",document)
        
        if arguments.o: 
            subprocess.run('open *jpeg',shell=True)

if __name__ == '__main__': 
    visualise()


