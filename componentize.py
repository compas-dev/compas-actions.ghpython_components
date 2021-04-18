from __future__ import print_function

import glob
import os

import clr

if __name__ == '__main__':
    here = os.path.dirname(__file__)
    libdir = os.path.join(here, 'lib')
    gh_io = os.path.join(libdir, 'GH_IO.dll')
    print('Running on {}'.format(here))
    print('Libs should be present under {}'.format(libdir))

    for f in glob.glob(os.path.join(libdir, '*.dll')):
        print('Found this:', f)
    try:
        clr.AddReferenceToFileAndPath(gh_io)
        print('Managed to find by path')
    except:
        clr.AddReference('GH_IO')
        print('Managed to find by ref name!')

    print('Done!')