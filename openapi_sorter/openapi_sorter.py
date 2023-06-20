import json
import re
import traceback
from time import perf_counter
from typing import List, Tuple

import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError, ValidatorDetectError
from yaml import YAMLError
from yaml.scanner import ScannerError


class OpenApiSorter:
    @classmethod
    def check_is_sorted(cls, items: list[str]) -> bool:
        return all([i for i in range(len(items) - 1) if items[i] <= items[i + 1]])

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

            print(f"{input_file}のソートを実施します")

            load_yaml_start_time = perf_counter()

            loaded_yaml = open(input_file, mode='r', encoding='utf_8')

            load_yaml_end_time = perf_counter()
            print(f"YAMLファイルの読み込みにかかった時間 → {load_yaml_end_time - load_yaml_start_time}秒")

            convert_dict_start_time = perf_counter()

            openapi_json = yaml.load(loaded_yaml, Loader=yaml.CSafeLoader)

            convert_dict_end_time = perf_counter()
            print(f"YAMLから辞書への変換にかかった時間 → {convert_dict_end_time - convert_dict_start_time}秒")

            sort_dict_start_time = perf_counter()

            for key, value in openapi_json.items():
                if key == 'paths':
                    paths = [path for path, _ in value.items()]
                    if not cls.check_is_sorted(items=paths):
                        paths = sorted(paths, key=lambda x: x)
                        new_value = {path: value.get(path) for path in paths}
                        openapi_json.update({'paths': new_value})
                elif key == 'components':
                    for component_key, component_value in value.items():
                        if component_key in ['requestBodies', 'schemas']:
                            keys = [key for key, _ in component_value.items()]
                            if not cls.check_is_sorted(items=keys):
                                keys = sorted(keys, key=lambda x: x)
                                new_value = {key: component_value.get(key) for key in keys}
                                value.update({component_key: new_value})
                elif key == 'tags':
                    if isinstance(value, List):
                        if not cls.check_is_sorted(items=[tag.get('name') for tag in value]):
                            openapi_json.update({'tags': sorted(value, key=lambda x: x.get('name'))})

            sort_dict_end_time = perf_counter()
            print(f"辞書のソートにかかった時間 → {sort_dict_end_time - sort_dict_start_time}秒")

            yaml.add_representer(str, cls._represent_str)

            # 時間計測のため辞書→yamlの変換とファイル書き込みを分離(.dumpで直接ファイル出力しない)

            dump_dict_start_time = perf_counter()

            dumped_yaml = yaml.dump(openapi_json, allow_unicode=True, sort_keys=False, indent=2, Dumper=yaml.CSafeDumper)

            dump_dict_end_time = perf_counter()
            print(f"辞書からYAMLの変換にかかった時間 → {dump_dict_end_time - dump_dict_start_time}秒")

            create_file_start_time = perf_counter()

            with open(
                output_file,
                mode='w',
                encoding='utf_8',
                newline='\n',
            ) as f:
                f.write(dumped_yaml)

            create_file_end_time = perf_counter()
            print(f"ファイル書き込みにかかった時間 → {create_file_end_time - create_file_start_time}秒")

        return not errors, errors

    # 「-」は先頭にある場合のみシングルクオーテーションが付与される

    @classmethod
    def _represent_str(cls, dumper, instance):
        if "\n" in instance:
            instance = "\n".join([line.rstrip() for line in instance.splitlines()])
            return dumper.represent_scalar('tag:yaml.org,2002:str', instance, style="|")
        elif isinstance(instance, str) and (re.match(r"-", instance) or re.search(r"[\[\]{}:\"]", instance)):
            return dumper.represent_scalar('tag:yaml.org,2002:str', instance, style="'")
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