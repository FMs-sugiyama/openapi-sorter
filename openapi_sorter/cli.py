import argparse
import sys

from openapi_sorter.openapi_sorter import OpenApiSorter


def main():
    parser = argparse.ArgumentParser(
        description='OpenAPI-Sorter is a utility for parsing, sorting,'
        ' and outputting OpenAPI YAML files by organizing path,'
        ' model, and other notations. It helps maintain clean and '
        'well-structured API documentation by ensuring consistent '
        'ordering of components in the YAML file.'
    )

    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument('inputs', metavar='FILE', nargs='+', help='one or more input files to process')

    group.add_argument('-o', '--output', help='Path to the output file')
    group.add_argument('--overwrite', action='store_true', help='Overwrite to the input file')

    parser.add_argument(
        '--allow-multiple',
        action='store_true',
        help='explicitly enable processing of multiple input files (only valid with --overwrite)',
    )

    args = parser.parse_args()

    if not args.allow_multiple and len(args.inputs) > 1:
        parser.error("processing multiple files requires the '--allow-multiple' option")

    if args.output and len(args.inputs) > 1:
        parser.error("the '--output' option can only be used when processing a single input file")

    kwargs = {}

    kwargs.update({'input_files': args.inputs})

    if args.output:
        kwargs.update({'output_file': args.output})
    elif args.overwrite:
        kwargs.update({'is_overwrite': args.overwrite})

    result, errors = OpenApiSorter.sort(**kwargs)

    if not result:
        for error in errors:
            print(error)

        sys.exit(1)
