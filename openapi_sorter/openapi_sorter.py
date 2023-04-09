from typing import List

import yaml


class OpenApiSorter:
    @classmethod
    def sort(cls, input_file: str, output_file: str = None, is_overwrite: bool = False):
        print(output_file)
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

        for key, value in openapi_json.items():
            if key == 'paths':
                paths = sorted([path for path, _ in value.items()], key=lambda x: x)

                new_value = {path: value.get(path) for path in paths}
                openapi_json.update({'paths': new_value})
            elif key == 'components':
                for component_key, component_value in value.items():
                    if component_key in ['requestBodies', 'schemas']:
                        keys = sorted([key for key, _ in component_value.items()], key=lambda x: x)
                        new_value = {key: component_value.get(key) for key in keys}
                        value.update({component_key: new_value})
            elif key == 'tags':
                if isinstance(value, List):
                    openapi_json.update({'tags': sorted(value, key=lambda x: x.get('name'))})

        yaml.add_representer(str, cls._represent_str)

        with open(
            output_file,
            mode='w',
            encoding='utf_8',
        ) as f:
            yaml.dump(openapi_json, f, allow_unicode=True, sort_keys=False)

    @classmethod
    def _represent_str(cls, dumper, instance):
        if "\n" in instance:
            return dumper.represent_scalar('tag:yaml.org,2002:str', instance, style='|')
        else:
            return dumper.represent_scalar('tag:yaml.org,2002:str', instance)
