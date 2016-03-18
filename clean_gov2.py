#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from boilerpipe.extract import Extractor

import logging
import traceback
import string
import nltk
from os import listdir, makedirs
from os.path import isfile, join, exists


class TrecReader:
    """
    Read trec web files and give document raw text
    """

    def __init__(self, file_path):
        self.f = open(file_path)

    def __iter__(self):
        return self

    def next(self):
        """
        :return: the next document
        """
        line = self.f.readline()  # <DOC>
        if not line:
            raise StopIteration()

        line = self.f.readline()  # <DOCNO>
        docno = line.strip().split('>')[1].split('<')[0]

        while True:
            line = self.f.readline().strip()
            if line == "</DOCHDR>":
                break
        lines = []
        while True:
            line = self.f.readline().strip()
            if line == "</DOC>":
                break
            lines.append(line)
        html_text = ' '.join(lines)
        return docno, html_text


def text_clean(text):
    res = text
    res = filter(lambda x: x in string.printable, res)

    ltoken = nltk.word_tokenize(res)
    for i in range(len(ltoken)):
        token = filter(lambda x: x.isalnum(), ltoken[i])
        ltoken[i] = token.lower()
    res = ' '.join(ltoken)
    res = ' '.join(res.split())
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_dir_path")
    parser.add_argument("out_file_path")
    args = parser.parse_args()

    f_names = [f for f in listdir(args.raw_dir_path)]
    fout = open(args.out_file_path, 'w')

    for f_name in f_names:
        trec_reader = TrecReader(join(args.raw_dir_path, f_name))
        empty_cnt = 0
        err_cnt = 0

        for docno, html_text in trec_reader:
            if not html_text:
                empty_cnt += 1
            try:
                extractor = Extractor(extractor='ArticleExtractor', html=html_text)
                text = extractor.getText()
                text = text.replace('\n', ' ').replace('\t', ' ')
                text = text.encode('ascii', 'ignore')
                text = text_clean(text)
                if text:
                    fout.write(docno + '\t' + text + '\n')
                else:
                    empty_cnt += 1
            except Exception as e:
                err_cnt += 1

    fout.close()
    print empty_cnt, err_cnt

if __name__ == '__main__':
    main()
