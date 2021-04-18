from __future__ import print_function

import glob
import os

import clr

if __name__ == '__main__':
    libdir = os.path.join(os.path.dirname(__file__), 'lib')
    gh_io = os.path.join(libdir, 'GH_IO.dll')

    for f in glob.glob(os.path.join(libdir, '*.dll')):
        print('Found this:', f)

    clr.AddReferenceToFileAndPath(gh_io)
    print('Done!')