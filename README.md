# OpenAPI-Sorter

OpenAPI-Sorter is a utility for parsing, sorting, and outputting OpenAPI YAML files by organizing path, model, and other notations. It helps maintain clean and well-structured API documentation by ensuring consistent ordering of components in the YAML file. Additionally, OpenAPI-Sorter can be used as a pre-commit hook to automatically sort OpenAPI YAML files during the commit process.

## Features

- Parse OpenAPI YAML files
- Sort path, model, and other notations within the YAML file
- Handle single or multiple input files
- Support output to a specified file or overwrite the original input files
- Pre-commit functionality to automatically sort and validate OpenAPI YAML files

## Installation

- coming soon

```
pip install openapi-sorter
```

## Usage

To sort a single OpenAPI YAML file and output the result:

```
python openapi_sorter_cli.py input_file.yaml --output output_file.yaml
```

To sort a single OpenAPI YAML file and overwrite the original:

```
python openapi_sorter_cli.py input_file.yaml --overwrite
```

To sort multiple OpenAPI YAML files and overwrite the originals:

```
python openapi_sorter_cli.py input_file1.yaml input_file2.yaml --overwrite --allow-multiple
```

### Pre-commit Hook

To use OpenAPI-Sorter as a pre-commit hook, follow these steps:

1. Install the pre-commit package:

```
pip install pre-commit
```

2. Create or update your `.pre-commit-config.yaml` file to include the OpenAPI-Sorter hook:

```yaml
repos:
  - repo: https://github.com/FMs-sugiyama/openapi-sorter
    rev: <desired_version>
    hooks:
      - id: openapi_sorter
        files: <target_files>
```

3. Install the pre-commit hook:

```
pre-commit install
```

With the pre-commit hook set up, OpenAPI-Sorter will automatically sort and validate OpenAPI YAML files during the commit process. If the YAML file is not a valid OpenAPI document, the commit will be aborted with an error message.

## Note

- The `--output` option can only be used when processing a single input file.
- The `--allow-multiple` option is required when processing multiple input files and can only be used with the `--overwrite` option.


## Contributing

Please feel free to submit issues or pull requests with any improvements or suggestions for this project.

## License

MIT License