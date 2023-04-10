#!/usr/bin/env python3
import sys

from openapi_sorter.openapi_sorter import OpenApiSorter


def format_files(file_paths):
    for file_path in file_paths:
        OpenApiSorter().sort(input_file=file_path, is_overwrite=True)


if __name__ == '__main__':
    format_files(sys.argv[1:])
