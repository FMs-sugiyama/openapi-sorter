#!/usr/bin/env python3

import sys

from openapi_sorter.openapi_sorter import OpenApiSorter


def format_files():
    file_paths = sys.argv[1:]

    errors = []
    for file_path in file_paths:
        result, error = OpenApiSorter().sort(input_file=file_path, is_overwrite=True)

        if not result:
            errors.append(error)

    if errors:
        sys.exit(1)
