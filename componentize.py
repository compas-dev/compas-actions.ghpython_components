from __future__ import print_function

import glob
import os

import clr

def find_ghio_assembly(libdir):
    for root, _dirs, files in os.walk(libdir):
        for basename in files:
            if basename == 'GH_IO.dll':
                print('Found!')
                filename = os.path.join(root, basename)
                return filename

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    libdir = os.path.join(here, 'lib')
    gh_io = find_ghio_assembly(libdir)

    print('GH_IO assembly found: {}'.format(gh_io))

    clr.AddReferenceToFileAndPath(gh_io)

    print('Done!')
