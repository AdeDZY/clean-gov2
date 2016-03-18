#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
import jobWriter

if __name__ == '__main__':
    corpus_fold = "./gov2-corpus/"

    clean_fold = "./gov2-cleaned/"
    if not exists(clean_fold):
        makedirs(clean_fold)

    dir_names = [f for f in listdir(corpus_fold)]
    executable = "./clean_gov2.sh"
    log = "/tmp/zhuyund_kmeans.log"
    out = "./clean_gov2.out"
    err = "./clean_gov2.err"

    njobs = 0
    jobfile = open("tmp.f", 'w')
    for dir_name in dir_names:

        input_dir_path = join(corpus_fold, dir_name)
        output_file_path = join(clean_fold, dir_name)

        arguments = "{0} {1}".format(input_dir_path, output_file_path)
        job = jobWriter.jobGenerator(executable, arguments, log, err, out)
        if njobs % 20 == 0:
            jobfile.close()
            jobfile = open("clean_gov2_{0}.job".format(njobs/20), 'w')
        jobfile.write(job)
        njobs += 1

    jobfile.close()
