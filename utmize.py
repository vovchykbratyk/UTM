"""
Main runner.

--CLI Usage--
utmize -f [file]
utmize -p [path]

Individual layers in container files may also be used with the -f switch; e.g.:

utmize -f C:/Temp/world_data.gpkg/continents
utmize -f C:/Temp/world_data.gdb/continents

"""

from convert import Converter
import getopt
import os
from pathlib import Path
import sys


def run_file(f):
    return Converter(f)


def run_path(p):
    converted = []
    ftypes = [
        '.shp', '.gpkg', '.tif', '.tiff',
        '.nitf', '.dt0', '.dt1', '.dt2',
        '.img', '.r0', '.gdb']
    files = [f for f in Path(p).rglob("**/*") if f.suffix in ftypes]
    for x in files:
        converted.append(Converter(x))

    return converted


if __name__ == '__main__':

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'f:p:')
        for opt, arg in opts:
            if opt in ['-f']:
                run_file(arg)
            elif opt in ['-p']:
                run_path(arg)
    except Exception as e:
        raise e
