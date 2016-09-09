#!/bin/env python
# coding=UTF-8

import struct
import string

def isTextFile(fq_file):
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    _null_trans = string.maketrans("", "")

    input_fq = open(fq_file)
    content = input_fq.read(1024)

    if "\0" in content:
        return False

    if not content:
        return True

    t = content.translate(_null_trans, text_characters)
    if float(len(t))/len(content) > 0.30:
        return False

    input_fq.close()
    return True


def fileType(fq_file):
    type_list = {"1F8B08": "gz"}
    input_fq = open(fq_file, 'rb')   #必须读二进制文件
    file_type = "unknown"
    for head_code in type_list.keys():
        numOfBytes = len(head_code)/2
        input_fq.seek(0)
        head_bytes = struct.unpack_from("B"*numOfBytes, input_fq.read(numOfBytes))
        file_head_code = bytes2hex(head_bytes)
        if file_head_code == head_code:
            file_type = type_list[head_code]
            break

    input_fq.close()
    return file_type

def bytes2hex(bytes):
    num = len(bytes)
    hex_str = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hex_str += u"0"
        hex_str += t
    return hex_str.upper()