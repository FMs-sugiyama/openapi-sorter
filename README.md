# OpenAPI-Sorter

OpenAPI-Sorter is a utility for parsing, sorting, and outputting OpenAPI YAML files by organizing path, model, and other notations. It helps maintain clean and well-structured API documentation by ensuring consistent ordering of components in the YAML file. Additionally, OpenAPI-Sorter can be used as a pre-commit hook to automatically sort OpenAPI YAML files during the commit process.

## Features

- Parse OpenAPI YAML files
- Sort path, model, and other notations within the YAML file
- Output the sorted YAML file or overwrite the original
- Pre-commit functionality to automatically sort and validate OpenAPI YAML files

## Installation

- coming soon

```
pip install openapi-sorter
```

## Usage

To sort an OpenAPI YAML file and output the result:

```
openapi_sorter input_file.yaml --output output_file.yaml
```

To sort an OpenAPI YAML file and overwrite the original file:

```
openapi_sorter input_file.yaml --overwrite
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
      - id: openapi-sorter
        files: <target_files>
```

3. Install the pre-commit hook:

```
pre-commit install
```

With the pre-commit hook set up, OpenAPI-Sorter will automatically sort and validate OpenAPI YAML files during the commit process. If the YAML file is not a valid OpenAPI document, the commit will be aborted with an error message.

## Contributing

Please feel free to submit issues or pull requests with any improvements or suggestions for this project.

## License

MIT License