#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Python-Tail - Unix tail follow implementation in Python.

python-tail  can be used to monitor changes to a file.

Example:
    import tail

    # Create a tail instance
    t = tail.Tail('file-to-be-followed')

    # Register a callback function to be a called when a new line is found in the folllowed file.
    # If no callback function is registerd, new lines would be printed to standard out.
    t.register_callback(callback_function)

    # Follow the file with 5 seconds as sleep time between iterations.
    # If sleep time is not provided 1 second is used as the default time.
    t.follow(s=5)

Reference:
    https://github.com/kasun/python-tail/blob/master/tail.py
    https://github.com/shengxinjing/pytail/blob/master/tail.py
'''

import os
import sys
import time

class Tail(object):
    ''' Represents a tail command. '''
    def __init__(self, tailed_file):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.

            Arguments:
                tailed_file - File to be followed. '''

        self.check_file_validity(tailed_file)
        self.tailed_file = tailed_file
        self.callback = sys.stdout.write

    def follow(self, n = 10, s = 1):
        ''' Do a tail follow. If a callback functin is registered it is called with every new line.
        Else printed to standard out.

        Arguments:
            s - Number of seconds to wait between each iteration; Defaults to 1. '''

        with open(self.tailed_file) as file_:
            self._file = file_
            # Go to the end of file
            file_.seek(0, 2)
            self.file_length = self.tell()
            self.showLastLine(n)
            while True:
                curr_postion = file_.tell()
                line = file_.readline()
                if not line:
                    file_.seek(curr_postion)
                    time.sleep(s)
                else:
                    self.callback(line)

    def showLastLine(self, n):
        # default 100 bytes per line.
        len_line = 100
        read_len = len_line * n
        while True:
            if read_len > self.file_length:
                self._file.seek(0)
                last_lines = self._file.read().split('\n')[-n:]
                break
            self._file.seek(-read_len, 2)
            last_words = self._file.read(read_len)
            count = last_words.count('\n')
            if count >= n:
                last_lines = last_words.split('\n')[-n:]
                break
            else:
                if count == 0:
                    len_perline = read_len
                else:
                    len_perline = read_len / count
                read_len = len_perline * n
        for line in last_lines:
            self.callback(line)

    def register_callback(self, func):
        ''' Overrides default callback function to provided function. '''
        self.callback = func

    def check_file_validity(self, file_):
        ''' Check whether the given file exists, readable and is a file '''
        if not os.access(file_, os.F_OK):
            raise TailError("File '%s' does not exist" % (file_))
        if not os.access(file_, os.R_OK):
            raise TailError("File '%s' not readable" % (file_))
        if os.path.isdir(file_):
            raise TailError("File '%s' is a directory" % (file_))

class TailError(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

