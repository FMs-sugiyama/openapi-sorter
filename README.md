# OpenAPI-Sorter

OpenAPI-Sorter is a utility for parsing, sorting, and outputting OpenAPI YAML files by organizing path, model, and other notations. It helps maintain clean and well-structured API documentation by ensuring consistent ordering of components in the YAML file.

## Features

- Parse OpenAPI YAML files
- Sort path, model, and other notations within the YAML file
- Output the sorted YAML file or overwrite the original

## Installation

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

## Contributing

Please feel free to submit issues or pull requests with any improvements or suggestions for this project.

## License

MIT License

