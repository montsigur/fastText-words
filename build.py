# Author: Wojciech Michałowski

from random import shuffle
from os.path import basename, abspath
from os import rename
from glob import glob
from optparse import OptionParser

def create_label(filepath, sep):

    filter_function = lambda s: len(s) > 1
    
    filename = ''.join(list(filter(filter_function, basename(filepath).split(sep)[0].replace(',', '').split())))
    
    label = '__label__' + filename

    return label
    
def create_training_files(path, outdir, sep='_', divide=False, punmarks='', lower=False, ratio=0.8):

    filepaths = glob(path)
    
    punmarks = punmarks.split('|')

    textblocks = []

    if outdir[-1] != '/':

        outdir += '/'
        
    for filepath in filepaths:

        label = create_label(filepath, sep) + ' , '
            
        with open(filepath) as file:

            contents = file.read()

            if lower:
                    
                contents = contents.lower()

            for mark in punmarks:

                contents = contents.replace(mark, '')

            contents = contents.split('\n')
                
            if divide:

                contents = [label + textblock + '\n' for textblock in contents]

                textblocks += contents

            else:

                contents = label + ' '.join(contents) + '\n'

                textblocks.append(contents)

    shuffle(textblocks)

    sep_index = int(len(textblocks) * ratio)

    with open(outdir + 'train.txt', 'w') as outfile:

        for textblock in textblocks[:sep_index]:

            outfile.write(textblock)

    with open(outdir + 'valid.txt', 'w') as outfile:

        for textblock in textblocks[sep_index:]:

            outfile.write(textblock)

if __name__ == '__main__':

    parser = OptionParser(usage='Usage: %prog [options] /path/to/directory/with/sample/documents')
    
    parser.add_option('-o', '--output', dest='outdir',
                      type=str, default='./',
                      help='Change the default directory of the output files (default is ./)')

    parser.add_option('-s', '--separator', dest='separator',
                      type=str, default='_',
                      help='Set the separator used to split sample files\' names. SEPARATOR is a single character.')

    parser.add_option('-p', '--punctuation-marks', dest='punctuation_marks',
                      type=str, default='.|,|(|)|\"|\'|;|:|-|[|]|!|?',
                      help='Get rid of punctuation marks in processed data. PUNCTUATION_MARKS is'\
                      + ' a sequence of punctuation marks separated by | (for example \'.|,|?|!\')')

    parser.add_option('-N', '--newline-split', dest='newline_split',
                      action='store_true',
                      help='Treat every newline in a sample file as a sample (construction of training data)')

    parser.add_option('-l', '--lower', dest='lower',
                      action='store_true',
                      help='Decapitalize the output text')

    parser.add_option('-r', '--train-valid-ratio', dest='ratio',
                      type=float, default=0.8,
                      help='Set the train-to-validation data size ratio. RATIO is a real value from 0 to 1.')
    
    opts, args = parser.parse_args()
    
    path = args[0] if args else None
            
    create_training_files(path, abspath(opts.outdir), opts.separator, opts.divide, opts.punmarks, opts.lower, opts.ratio)
