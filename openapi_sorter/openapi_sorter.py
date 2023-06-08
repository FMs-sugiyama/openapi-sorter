import json
import re
import traceback
from pprint import pprint
from typing import List, Optional, Tuple, Any

import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError, ValidatorDetectError
from yaml import YAMLError
from yaml.scanner import ScannerError


class OpenApiSorter:
    _targets: List[str] = []

    @classmethod
    def _check_paths(cls, paths: dict):
        for path_name, path_items in paths.items():
            if re.search(r'{[a-zA-Z0-9]+}', path_name):
                cls._targets.append(path_name)

    @classmethod
    def _check_properties(cls, properties: dict):
        for property_item in properties.values():
            if example := property_item.get("example"):
                if property_type := property_item.get("type"):
                    if property_type == "string" and (re.match(r"-", example) or re.search(r"[\[\]{}:\"]", example)):
                        cls._targets.append(example)

    @classmethod
    def _check_components(cls, components):
        schemas = components.get("schemas")

        if not schemas:
            return

        for schema_item in schemas.values():
            if properties := schema_item.get("properties"):
                cls._check_properties(properties=properties)

            if all_of_items := schema_item.get("allOf"):
                for all_of_item in all_of_items:
                    if properties := all_of_item.get("properties"):
                        cls._check_properties(properties=properties)

    @classmethod
    def _check_servers(cls, servers: list[dict]):
        for server in servers:
            if url := server.get("url"):
                cls._targets.append(url)
            if description := server.get("description"):
                cls._targets.append(description)

    @classmethod
    def sort(
        cls, input_files: List[str], output_file: str = None, is_overwrite: bool = False
    ) -> Tuple[bool, List[str]]:
        errors = []

        for input_file in input_files:
            if not cls.is_valid_yaml(input_file=input_file):
                errors.append(f'{input_file} is not YAML file.')
                continue

            if not cls.is_valid_openapi(input_file=input_file):
                errors.append(f'{input_file} is not OpenAPI file.')
                continue

            if is_overwrite:
                output_file = input_file

            openapi_json = yaml.load(
                open(
                    input_file,
                    mode='r',
                    encoding='utf_8',
                ),
                Loader=yaml.SafeLoader,
            )

            # 1ファイルごとに初期化
            cls._targets = []

            for key, value in openapi_json.items():
                if key == 'paths':
                    cls._check_paths(paths=value)
                    paths = sorted([path for path, _ in value.items()], key=lambda x: x)
                    new_value = {path: value.get(path) for path in paths}
                    openapi_json.update({'paths': new_value})
                elif key == 'components':
                    cls._check_components(components=value)
                    for component_key, component_value in value.items():
                        if component_key in ['requestBodies', 'schemas']:
                            keys = sorted([key for key, _ in component_value.items()], key=lambda x: x)
                            new_value = {key: component_value.get(key) for key in keys}
                            value.update({component_key: new_value})
                elif key == 'tags':
                    if isinstance(value, List):
                        openapi_json.update({'tags': sorted(value, key=lambda x: x.get('name'))})
                elif key == 'servers':
                    cls._check_servers(servers=value)

            yaml.add_representer(str, cls._represent_str)

            with open(
                output_file,
                mode='w',
                encoding='utf_8',
                newline='\n',
            ) as f:
                yaml.dump(openapi_json, f, allow_unicode=True, sort_keys=False, indent=2)

        return not errors, errors

    @classmethod
    def _represent_str(cls, dumper, instance):
        if instance in cls._targets:
            return dumper.represent_scalar('tag:yaml.org,2002:str', instance, style="'")
        elif "\n" in instance:
            return dumper.represent_scalar('tag:yaml.org,2002:str', instance, style='|')
        else:
            return dumper.represent_scalar('tag:yaml.org,2002:str', instance)

    @classmethod
    def is_valid_openapi(cls, input_file: str) -> bool:
        try:
            # If no exception is raised by validate_spec(), the spec is valid.
            spec_dict, spec_url = read_from_filename(input_file)

            # validate_spec(spec_dict)

            return True
        except (OpenAPIValidationError, ValidatorDetectError):
            traceback.print_exc()
            return False

    @classmethod
    def is_valid_yaml(cls, input_file: str):
        try:
            with open(input_file, "r") as file:
                data = yaml.safe_load(file)
            return data is not None
        except (YAMLError, ScannerError):
            return False
