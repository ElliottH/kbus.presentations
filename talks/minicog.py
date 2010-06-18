#! /usr/bin/env python

"""A (very much) more primitive equivalent of Ned Batchelder's cog

(by the way, cog itself is really neat and you should check it out)

Usage: minicog.py <infile> [<outfile>]

If <outfile> is '-' then it stdout will be used.

We're more primitive because we don't do many of the things cog does,
especially handling non-reStructuredText markup, retaining the original
code, and being able to write (back) to the original file.

On the other hand, our markup is just::

    .. [[[
    <code to run>
    .. ]]]

Indentation within a single "block" must be consistent with the first
line. All lines in the "block" must start with at least 3 spaces, and
also at least the same number of spaces as the first line of the "block".
"""

import sys
import os
import StringIO

outputter = StringIO.StringIO()

def canonical_path(path):
    path = os.path.expandvars(path)       # $NAME or ${NAME}
    path = os.path.expanduser(path)       # ~
    path = os.path.normpath(path)
    path = os.path.abspath(path)          # copes with ., thing/../fred, etc.
    return path

class Reader(object):

    def __init__(self, infd):
        self.infd = infd
        self.line = None
        self.line_num = 0

    def next_line(self):
        self.line_num += 1
        self.line = self.infd.readline()
        if self.line:
            return self.line
        else:
            raise StopIteration     # end-of-file

    def indent_error(self, expected_indent):
        print 'Stopping - line %d appears wrongly indented'%self.line_num
        print 'Expecting indentation of %d, got %d'%(expected_indent,
                calc_indent(self.line))
        print '"%s"'%self.line.rstrip()
        raise StopIteration

def calc_indent(line):
    indent_len = 0
    while line[indent_len] == ' ':
        indent_len += 1
    return indent_len

def get_next_generator(reader, globals, verbose=True):
    blocknum = 0
    while True:
        line = reader.next_line()
        if line.startswith('.. [[['):
            if verbose:
                blocknum += 1
                print 'Code block %d'%blocknum
            indent_len = indent_str = None
            codelines = []
            line = reader.next_line()
            while not line.startswith('.. ]]]'):
                if not line.strip():
                    # Empty line - just accept it as is
                    # (do we care? should we really just ignore it?)
                    codelines.append('')
                elif line.startswith('   '):    # minimum for an rst comment
                    if indent_str:
                        if not line.startswith(indent_str):
                            reader.indent_error(indent_len)
                    else:
                        indent_len = calc_indent(line)
                        indent_str = indent_len * ' '
                    codelines.append(line[indent_len:].rstrip())
                else:
                    reader.indent_error(3)
                line = reader.next_line()
            codelines.append('')
            try:
                sys.stdout = outputter
                exec '\n'.join(codelines) in globals
            except:
                sys.stdout = sys.__stdout__
                print 'Stopping - error in code block ending at line',reader.line_num
                raise
            finally:
                sys.stdout = sys.__stdout__
            result = outputter.getvalue()
            outputter.truncate(0)
            yield result
        else:
            yield line

def process(infd, outfd, verbose=True):
    reader = Reader(infd)
    get_next = get_next_generator(reader, {}, verbose)
    for text in get_next:
        outfd.write(text)

def main(args):

    if len(args) == 0 or args[0] in ('-help', '--help', '-h'):
        print __doc__
        return

    if len(args) == 2:
        infile = args[0]
        outfile = args[1]
    elif len(args) == 1:
        infile = args[0]
        outfile = '%s.tmp'%os.path.splitext(infile)[0]
    else:
        print __doc__
        return

    if outfile != '-' and canonical_path(infile) == canonical_path(outfile):
        print "Input and output are the same (%s) - shan't."%canonical_path(infile)
        return

    print 'Input: ',infile
    print 'Output:',outfile if outfile != '-' else '<stdout>'

    with open(infile) as infd:
        if outfile == '-':
            process(infd, sys.stdout, verbose=False)
        else:
            with open(outfile,'w') as outfd:
                process(infd, outfd)

if __name__ == '__main__':
    main(sys.argv[1:])

# vim: set tabstop=8 softtabstop=4 shiftwidth=4 expandtab:
