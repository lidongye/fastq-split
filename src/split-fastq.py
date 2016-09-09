#!/user/bin/env python
import os
from optparse import OptionParser
import gzip
import re

import common_function

def get_length(line):
    """
    get length from first line

    :param line:
    :return:
    """

    n = 202
    return n

def split_line0(line):
    """
    split first line to two lines

    :param line: first line fastq
    :return: two lines
    """

    if re.search(r'length=\d+', line):
        seq_length = int(re.findall(r'length=(\d+)', line)[0])
        line_cut = re.sub(r'length=\d+', 'length=' + str(seq_length / 2), line)
    else:
        line_cut = line
    return [line_cut, line_cut]


def split_line1(line):
    """
    split second line to two lines

    :param line: first line fastq
    :return: two lines
    """

    num = len(line)
    line_0 = line[:num / 2]
    line_1 = line[num / 2:]
    return [line_0, line_1]

def split_line2(line):
    """
    split third line to two lines

    :param line: first line fastq
    :return: two lines
    """

    if re.search(r'length=\d+', line):
        seq_length = int(re.findall(r'length=(\d+)', line)[0])
        line_cut = re.sub(r'length=\d+', 'length=' + str(seq_length / 2), line)
    else:
        line_cut = line
    return [line_cut, line_cut]


def split_line3(line):
    """
    split fourth line to two lines

    :param line: first line fastq
    :return: two lines
    """

    num = len(line)
    line_0 = line[:num / 2]
    line_1 = line[num / 2:]
    return [line_0, line_1]


def get_output_filenames(input_fastq):
    """
    create out paired end file names

    :param input_fastq:
    :return:
    """
    [file_name, ext] = os.path.splitext(input_fastq)
    return ["%s_1%s" % (file_name, ext), "%s_2%s" % (file_name, ext)]


def split_fastq(input_fastq):
    """
    split single-end fastq file to paired-end fastq files

    :param input_fastq: input single-end fastq file
    :return: None
    """

    [out_file1, out_file2] = get_output_filenames(input_fastq)
    if common_function.isTextFile(input_fastq):
        fq_input = open(input_fastq)
        fq_output1 = open(out_file1, 'w')
        fq_output2 = open(out_file2, 'w')
    elif common_function.fileType(input_fastq) == "gz":
        fq_input = gzip.open(input_fastq)
        fq_output1 = gzip.open(out_file1, 'w')
        fq_output2 = gzip.open(out_file2, 'w')
    while True:
        line0 = fq_input.readline().split('\n')[0]
        if line0 == "":
            break
        line1 = fq_input.readline().split('\n')[0]
        line2 = fq_input.readline().split('\n')[0]
        line3 = fq_input.readline().split('\n')[0]

        [line0_1, line0_2] = split_line0(line0)
        [line1_1, line1_2] = split_line1(line1)
        [line2_1, line2_2] = split_line2(line2)
        [line3_1, line3_2] = split_line3(line3)
        fq_output1.writelines([line+'\n' for line in [line0_1, line1_1, line2_1, line3_1]])
        fq_output2.writelines([line+'\n' for line in [line0_2, line1_2, line2_2, line3_2]])

    fq_input.close()
    fq_output1.close()
    fq_output2.close()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--input_fastq", dest="input_fastq",
                      help="single end fastq file")
    (options, args) = parser.parse_args()
    input_fastq = options.input_fastq

    split_fastq(input_fastq)