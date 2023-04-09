import argparse

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

    group.add_argument('-o', '--output', help='Path to the output file')
    group.add_argument('--overwrite', action='store_true', help='Overwrite to the input file')

    parser.add_argument('input', help='Path to the input file')

    args = parser.parse_args()

    kwargs = {}

    kwargs.update({'input_file': args.input})

    if args.output:
        kwargs.update({'output_file': args.output})
    elif args.overwrite:
        kwargs.update({'is_overwrite': args.overwrite})

    OpenApiSorter.sort(**kwargs)


if __name__ == '__main__':
    main()
