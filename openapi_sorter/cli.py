import argparse


def main():
    parser = argparse.ArgumentParser(description='OpenAPI-Sorter is a utility for parsing, sorting,'
                                                 ' and outputting OpenAPI YAML files by organizing path,'
                                                 ' model, and other notations. It helps maintain clean and '
                                                 'well-structured API documentation by ensuring consistent '
                                                 'ordering of components in the YAML file.')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-o', '--output', help='Path to the output file')
    group.add_argument('--overwrite', action='store_true', help='Overwrite to the input file')

    parser.add_argument('input', help='Path to the input file')

    args = parser.parse_args()

    # Call your main function or script with the provided argument
    print(args.input)

    if args.output:
        print(args.output)
        # your_main_function(arg1=args.arg1)
    elif args.overwrite:
        print(args.overwrite)
        pass
        # your_main_function(arg2=args.arg2)


if __name__ == '__main__':
    main()