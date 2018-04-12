# Author: Wojciech Michałowski

import numpy as np
from build import *
from os.path import basename, abspath, isdir, curdir
from os import environ, system, remove
from glob import glob
from optparse import OptionParser
import codecs
import sys

FASTTEXT_PATH = environ['FASTTEXT_PATH'] # path to fasttext executable    

def cluster(means, data, distance):

    clusters = [list() for i in range(len(means))]
    
    for vector in data:
                
        clusters[np.argmin([distance(vector, mean)\
                            for mean in means])].append(vector)

    return clusters

def files_modification_consent(files):

    message = 'Following files will be overwritten and removed (if they exist):\n'\
              + '\n'.join([abspath(curdir) + '/' + file for file in files])\
              + '\nContinue? (y/n) '
    
    answer = input(message)

    if answer != 'y':

        exit(0)

def assert_isfile(path):

    if isdir(path) and path != '-':

        print('-o: provided path is a directory, it must be a path to a file')

        exit(-1)
        
if __name__ == "__main__":

    parser = OptionParser(usage='Usage: %prog [options] directory_with_samples\n'\
                              + '       %prog [options] model_vec model_bin\n'\
                              + '       %prog [options] -d dump_file model_vec\n')

    parser.add_option('-w', '--words-count', dest='words_count',
                      type=int, default=15,
                      help='Number of most fit words to display')
    
    parser.add_option('-o', '--output', dest='output',
                      type=str, default='-',
                      help='Change the destination of the program output. OUTPUT is a path to an output file.')

    parser.add_option('-D', '--document', dest='docpath',
                      type=str, default=None,
                      help='Print words from a document at path DOCPATH that are best fit for its label'\
                      + ' (instead of words and all labels from the whole fasttext model)')

    parser.add_option('-d', '--dump-file', dest='dump_file',
                      type=str, default=None,
                      help='Provide a file generated with mkdumpfile (saves time). DUMP_FILE is a dump file\'s path.')
    
    parser.add_option('-p', '--punctuation-marks', dest='punctuation_marks',
                      type=str, default='.|,|(|)|\"|\'|;|:|-|[|]|!|?',
                      help='Get rid of punctuation marks in processed data. PUNCTUATION_MARKS is'\
                      + ' a sequence of punctuation marks separated by | (for example \'.|,|?|!\')')

    parser.add_option('-W', '--print-weights', dest='print_weights',
                      action='store_true', default=False,
                      help='Print weights of the output words')

    parser.add_option('-q', '--quiet', dest='quiet',
                      action='store_true', default=False,
                      help='Prevent the program from printing information about progress')

    parser.add_option('-N', '--newline-split', dest='newline_split',
                      action='store_true',
                      help='Treat every newline in a sample file as a sample (construction of training data)')

    parser.add_option('-s', '--separator', dest='separator',
                      type=str, default='_',
                      help='Set the separator used to split sample files\' names. SEPARATOR is a single character.')

    parser.add_option('-l', '--lower', dest='lower',
                      action='store_true',
                      help='Decapitalize the processed data')

    parser.add_option('-r', '--train-valid-ratio', dest='ratio',
                      type=float, default=0.8,
                      help='Set the train-to-validation data size ratio. RATIO is a real value from 0 to 1.')

    parser.add_option('-k', '--keep-model', dest='keep_model',
                      action='store_true',
                      help='Keep the model created by the program after it exits')
    
    parser.add_option('-y', '--answer-yes', dest='answer_yes',
                      action='store_true',
                      help='Answer \'yes\' to all questions')
    
    opts, args = parser.parse_args()
    
    if len(args) < 1:

        if not opts.quiet:

            print(parser.format_help())
            
        exit(-1)

    elif isdir(args[0]):

        assert_isfile(opts.output)
        
        if not opts.answer_yes:
        
            if not opts.dump_file:

                files = ['dump_output.vec', 'dump_dict.vec', 'train.txt', 'validate.txt']

            else:

                files = ['train.txt', 'validate.txt']

            if not opts.keep_model:

                files += ['model.bin', 'model.vec']
                
            files_modification_consent(files)

        if not opts.quiet:
                
            print('Creating training and validation files ...', end='\r')

        training_data_path = abspath('./')
            
        create_training_files(args[0] + '*',
                              abspath(training_data_path),
                              opts.separator,
                              opts.newline_split,
                              opts.punctuation_marks,
                              opts.lower,
                              opts.ratio)

        if not opts.quiet:
            
            print('Creating training and validation files... done')
        
            print('Training fasttext model ...')
        
        system(FASTTEXT_PATH + ' supervised -input ' + training_data_path + '/train.txt' + ' -output model -epoch 25 -lr 1.0'\
               + (' -verbose 0' if opts.quiet else ''))

        if not opts.quiet:
                
            print('Done training fasttext model')
        
        model_bin_path = abspath('./model.bin')
        model_vec_path = abspath('./model.vec')

        remove(training_data_path + '/train.txt')
        remove(training_data_path + '/valid.txt')
        
    elif opts.dump_file:

        assert_isfile(opts.output)
        
        model_vec_path = args[0]

    elif len(args) < 2:

        if not opts.quiet:

            print(parser.format_help())
            
        exit(-1)
        
    else:

        assert_isfile(opts.output)
        
        if not opts.answer_yes:
        
            files = ['dump_dict.vec', 'dump_output.vec']

            files_modification_consent(files)
            
        model_vec_path = args[0]
        model_bin_path = args[1]
        
    with codecs.open(model_vec_path, encoding='utf-8') as file:

        if not opts.quiet:
            print('Reading ' + basename(model_vec_path) + ' ...', end='\r')

        data = file.read()
        
        if not opts.quiet:
            print('Reading ' + basename(model_vec_path) + ' ... done')
        
    if not opts.keep_model:

        remove(model_vec_path)

    data = data.replace(u'\xa0', u'').split('\n')[:-1]

    # meta_data = np.array(data[0].split(), dtype=np.int)

    if not opts.quiet:
        print('Preprocessing data from '\
              + basename(model_vec_path) + ' ...', end='\r')
        
    vectors = []
    
    for line in data[1:]:
        
        try:
            
            vector = (line.split()[0], np.array(line.split()[1:], dtype=np.double))

        except:
            
            vector = (line.split()[0], np.array(line.split()[2:], dtype=np.double))
            
        vectors.append(vector)

    if not opts.quiet:
        print('Preprocessing data from '\
              + basename(model_vec_path) + ' ... done')

    words_hash_table = {}
    words_dict = {}

    if not opts.quiet:
        print('Creating hash table for all words from the model ...', end='\r')

    for word_vector_pair in vectors:
        
        words_hash_table[str(word_vector_pair[1])] = word_vector_pair[0]
        words_dict[word_vector_pair[0]] = word_vector_pair[1]

    if not opts.quiet:
        print('Creating hash table for all words from the model... done')
        
    vectors = [word_vector_pair[1] for word_vector_pair in vectors]

    if not opts.dump_file:

        system(FASTTEXT_PATH + ' dump ' + model_bin_path + ' output > dump_output.vec')

        with codecs.open('dump_output.vec', encoding='utf-8') as file:

            dump_output = file.read()

        remove('dump_output.vec')

        system(FASTTEXT_PATH + ' dump ' + model_bin_path + ' dict > dump_dict.vec')

        with codecs.open('dump_dict.vec', encoding='utf-8') as file:

            dump_dict = file.read()

        remove('dump_dict.vec')

        if not opts.keep_model:

            remove(model_bin_path)
        
        labels_vectors = np.array([np.array(list(map(np.double, vector.split())))\
                                   for vector in dump_output.strip().split('\n')[1:]])

        labels = [line.split()[0] for line in dump_dict.strip().split('\n')[-len(labels_vectors):]]
        
        labels_with_vectors = list(zip(labels, labels_vectors))    

    else:
        
        with codecs.open(opts.dump_file, encoding='utf-8') as file:
            
            if not opts.quiet:
                print('Reading ' + basename(opts.dump_file) + ' ...', end='\r')
                
            data = file.read()
            
            if not opts.quiet:
                print('Reading ' + basename(opts.dump_file) + ' ... done')

        data = data.replace(u'\xa0', u'').split('\n')[:-1]
        labels_with_vectors = [(line.split()[0], np.array(line.split()[1:], dtype=np.double))\
                               for line in data]

        labels_vectors = np.array([label_vector_pair[1] for label_vector_pair in labels_with_vectors])
        labels = [label_vector_pair[0] for label_vector_pair in labels_with_vectors]

    labels_hash_table = {}
    labels_dict = {}
    
    for label_vector_pair in labels_with_vectors:
        
        labels_hash_table[str(label_vector_pair[1])] = label_vector_pair[0]
        labels_dict[label_vector_pair[0]] = label_vector_pair[1]

    distance = lambda x, y: 1 - np.exp(np.dot(x[:min(len(x), len(y))], y[:min(len(x), len(y))]))\
               / np.exp(x[:min(len(x), len(labels_vectors[0]))]\
                        * labels_vectors[:, :min(len(x), len(labels_vectors[0]))]).sum()

    if opts.docpath:

        with codecs.open(opts.docpath, encoding='utf-8') as file:

            if not opts.quiet:
                print('Reading document file ...', end='\r')
            data = file.read()
            if not opts.quiet:
                print('Reading document file... done')

        for mark in opts.punctuation_marks:

            data = data.replace(mark, '')

        document_words = list(set(data.lower().split()))

        document_label = create_label(opts.docpath, '_')

        label_vector = labels_dict[document_label]

        word_distance_pairs = []

        key_func = lambda x: x[1]
        
        for word in document_words:

            if word in words_dict.keys():

                word_distance_pairs.append((word, distance(words_dict[word], label_vector)))

        word_distance_pairs = sorted(word_distance_pairs, key=key_func)

    else:

        if not opts.quiet:

            print('Clustering ...', end='\r')
        
        clusters = cluster(labels_vectors, vectors, distance)
    
        labels_count = len(labels_vectors)
        
        if not opts.quiet:

            print('Clustering ... done')
    
        key_func = lambda x: x[1]
        
        for i in range(labels_count):

            if not opts.quiet:
                print('Processing cluster no %d (calculating distances) ...' %(i+1), end='\r')
            clusters[i] = [(word_vector, distance(word_vector, labels_vectors[i]))\
                           for word_vector in clusters[i]]
            if not opts.quiet:
                print('Processing cluster no %d (sorting) ...              ' %(i+1), end='\r')

            clusters[i] = sorted(clusters[i], key=key_func)

            if not opts.quiet:
                print('Processing cluster no %d ... done                   ' %(i+1), end=('\n'\
                if i == labels_count-1 else '\r'))

    if opts.output == '-':

        if not opts.quiet:
            print()
        
        file = sys.stdout
            
    else:

        file = open(opts.output, 'w')

    if opts.docpath:

        print(document_label)
        
        for word_distance_pair in word_distance_pairs[:opts.words_count]:
            
            print(word_distance_pair[0], str(1 - word_distance_pair[1]) if opts.print_weights else '', file=file)

    else:
        
        print(','.join([labels_hash_table[str(label_vector)] for label_vector in labels_vectors]), file=file)
        
        for i in range(opts.words_count):

            print(','.join([words_hash_table[str(cluster[i][0])] for cluster in clusters]), file=file)

    if opts.output != '-':
        
        file.close()
