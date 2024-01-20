import argparse
import base64
import json
import os
import re
import sys
import tempfile
import urllib.request, urllib.parse, urllib.error
import zipfile
from io import StringIO

import clr
import System
import System.IO




def main():
    from GH_IO.Serialization import GH_LooseChunk
    
    # get all the types and corresponding guids
    # rewrite this: 08908df5-fa14-4982-9ab2-1aa0927566aa in majuscule
    # i ncomment the line below
    print(GH_LooseChunk.GetKnownTypes())



if "__main__" == __name__:

    gh_io : str = r"C:\Users\andre\.nuget\packages\grasshopper\8.0.23164.14305-wip\lib\net48\GH_IO.dll"
    gh_io = os.path.abspath(gh_io)
    gh_io = gh_io[:-4]
    clr.AddReference(gh_io)


    main()