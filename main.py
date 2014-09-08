from __future__ import division

import glob
import os

import pyprind
import pandas as pd

from text_comp_utils.utils import *
from text_comp_utils.argconfig import *
from text_comp_utils.usage_tests import *


def main():
    args = read_configuration_options()

    files_to_process = glob.glob(os.path.join('texts', '*.txt'))
    print 'Found {} files...'.format(len(files_to_process))

    out_array = [[] for x in range(int(args.iterations)+1)]

    for i, fname in enumerate(files_to_process):
        out_array[0].append(fname.split('/')[1].replace('.txt',''))
        # print '\n'
        print 'Testing File: {}'.format(fname).upper()
        # tokenize the file
        tokens = tokenize(depunctuate(ingest(fname)))
        print '  - Interpreted {} word-tokens'.format(len(tokens))
        chunk_size = int(len(tokens) * args.sample)
        print '  - Sample based on {} words ({:.0%} of full text)'.format(chunk_size, args.sample)

        # print '\n'
        # test bag of words method
        print '  - Testing "bag-of-words" method'

        bow_results = []
        prbar = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        for x in xrange(int(args.iterations)):
            r = compare_stop_word_usage(tokens, args.sample, args.absolute, method=1)[0]
            out_array[x+1].append(r)
            bow_results.append(r)
            prbar.update()
        summarize_results(bow_results, 'Chi2')
        #write_result(bow_results, fname.replace('.txt', '') + '_bow_result.csv')
        print '\n'

        # test paired samples method
       # print '\n'
       # print '-----------------------------------------'
       # print '-- Testing \'paired random chunks\' method --'
       # print '-----------------------------------------'
       # mul_bags = []
       # prbar3 = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
       # for x in range(int(args.iterations)):
       #     mul_bags.append(test_random_paired_chunks(tokens, args.sample)[0])
       #     prbar3.update()
       # summarize_results(mul_bags, 'Chi2')
       # write_result(mul_bags, fname.replace('.txt', '') + '_mulbow_result.csv')
    write_output('test.txt',out_array)
    #data = out_array
    #df = pd.DataFrame(data[1:], columns=data[0])
    #import matplotlib.pyplot as plt
    #pd.options.display.mpl_style = 'default'
    #plt.figure()
    #df.diff().hist(color='k',alpha=.5, bins=50)
    #df.plot()
if __name__ == '__main__':
    main()
