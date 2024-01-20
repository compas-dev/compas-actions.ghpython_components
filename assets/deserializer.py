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
    
    # ghuser_path : str = r"F:\compas-actions.ghpython_components\assets\TestUserObjectCpy.ghuser"  # cpy
    ghuser_path : str = r"F:\compas-actions.ghpython_components\build\Test_KitchenSink.ghuser"    # ipy
    
    deserialized_data = GH_LooseChunk("UserObject")

    data_bytes = System.IO.File.ReadAllBytes(ghuser_path)

    # get if the data_bytes is empty
    if data_bytes:
        deserialized_data.Deserialize_Binary(data_bytes)
    else:
        deserialized_data = None
        print("No data found in file")

    deserialized_data.Deserialize_Binary(data_bytes)

    # convert to xml
    xml = deserialized_data.Serialize_Xml()


    print(xml)




if "__main__" == __name__:

    gh_io : str = r"C:\Users\andre\.nuget\packages\grasshopper\8.0.23164.14305-wip\lib\net48\GH_IO.dll"
    gh_io = os.path.abspath(gh_io)
    gh_io = gh_io[:-4]
    clr.AddReference(gh_io)


    main()