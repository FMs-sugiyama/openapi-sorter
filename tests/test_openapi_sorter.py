import tempfile
from unittest import TestCase

import yaml

import pytest
from openapi_sorter.openapi_sorter import OpenApiSorter


class TestOpenApiSorter(TestCase):
    @pytest.fixture(autouse=True)
    def create_openapi_yaml(self):
        openapi_str = '''
openapi: 3.0.0
x-stoplight:
  id: vhpofek51ivt0
info:
  title: openapi-sorter test yaml
  version: '1.0'
  description: |-
    test
    テスト
servers:
  - url: 'http://localhost:3000'
paths:
  /charlie:
    get:
      summary: Your GET endpoint
      tags: []
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Charlie'
      operationId: get-charlie
  /bravo:
    get:
      summary: Your GET endpoint
      tags: []
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Bravo'
      operationId: get-bravo
  /alpha:
    get:
      summary: Your GET endpoint
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Alpha'
      operationId: get-alpha
components:
  schemas:
    Charlie:
      title: Charlie
      x-stoplight:
        id: ufu49301wme48
      type: object
      properties:
        id:
          type: string
    Alpha:
      title: Alpha
      x-stoplight:
        id: nsearplc0j3py
      type: object
      properties:
        id:
          type: string
    Bravo:
      title: Bravo
      x-stoplight:
        id: jcjy76yd8l41n
      type: object
      properties:
        id:
          type: string
  requestBodies:
    CharlieBody:
      content:
        application/json:
          schema:
            type: object
    BravoBody:
      content:
        application/json:
          schema:
            type: object
    AlphaBody:
      content:
        application/json:
          schema:
            type: object
tags:
  - name: alpha
  - name: bravo
  - name: charlie
'''
        try:
            with tempfile.NamedTemporaryFile() as src, open(src.name, 'w') as input_file:
                self.input_file_name = src.name

                input_file.write(openapi_str)
                input_file.flush()

                with tempfile.NamedTemporaryFile() as origin, open(origin.name, 'w') as origin_file:
                    self.original_file_name = origin.name

                    origin_file.write(openapi_str)
                    origin_file.flush()

                    yield

        finally:
            pass

    def test_sort_no_sort(self):
        with tempfile.NamedTemporaryFile() as src, open(src.name, 'w') as dummy_file:
            dummy_file.write('')
            dummy_file.flush()

            result, errors = OpenApiSorter.sort(input_files=[dummy_file.name], is_overwrite=True)

            assert not result
            assert errors == [f'{dummy_file.name} is not YAML file.']

        with tempfile.NamedTemporaryFile() as src, open(src.name, 'w') as dummy_file:
            dummy_file.write('a')
            dummy_file.flush()

            result, errors = OpenApiSorter.sort(input_files=[dummy_file.name], is_overwrite=True)

            assert not result
            assert errors == [f'{dummy_file.name} is not OpenAPI file.']

        with tempfile.NamedTemporaryFile() as src, open(src.name, 'w') as dummy_file:
            dummy_file.write('alpha: bravo')
            dummy_file.flush()

            result, errors = OpenApiSorter.sort(input_files=[dummy_file.name], is_overwrite=True)

            assert not result
            assert errors == [f'{dummy_file.name} is not OpenAPI file.']

        with tempfile.NamedTemporaryFile() as src, open(src.name, 'w') as dummy_file:
            dummy_file.write(
                '''
key1: value1
  key2: value2
'''
            )
            dummy_file.flush()

            result, errors = OpenApiSorter.sort(input_files=[dummy_file.name], is_overwrite=True)

            assert not result
            assert errors == [f'{dummy_file.name} is not YAML file.']

    def test_sort_overwrite(self):
        result, errors = OpenApiSorter.sort(input_files=[self.input_file_name], is_overwrite=True)

        assert result
        assert not errors

        openapi_json = yaml.load(
            open(
                self.input_file_name,
                mode='r',
                encoding='utf_8',
            ),
            Loader=yaml.SafeLoader,
        )

        original_openapi_json = yaml.load(
            open(
                self.original_file_name,
                mode='r',
                encoding='utf_8',
            ),
            Loader=yaml.SafeLoader,
        )

        self.assert_paths(openapi_json, original_openapi_json)

        self.assert_component_request_bodies(openapi_json, original_openapi_json)

        self.assert_tags(openapi_json, original_openapi_json)

        self.assert_others(openapi_json, original_openapi_json)

    def test_sort_output(self):
        with tempfile.NamedTemporaryFile() as dest:
            result, errors = OpenApiSorter.sort(input_files=[self.input_file_name], output_file=dest.name)

            assert result
            assert not errors

            openapi_json = yaml.load(
                open(
                    dest.name,
                    mode='r',
                    encoding='utf_8',
                ),
                Loader=yaml.SafeLoader,
            )

            original_openapi_json = yaml.load(
                open(
                    self.input_file_name,
                    mode='r',
                    encoding='utf_8',
                ),
                Loader=yaml.SafeLoader,
            )

            self.assert_paths(openapi_json, original_openapi_json)

            self.assert_component_request_bodies(openapi_json, original_openapi_json)

            self.assert_tags(openapi_json, original_openapi_json)

            self.assert_others(openapi_json, original_openapi_json)

    @classmethod
    def assert_paths(cls, openapi_json, original_openapi_json):
        paths = openapi_json.get('paths')
        assert len(paths) == 3

        keys = list(paths.keys())
        assert keys[0] == '/alpha'
        assert keys[1] == '/bravo'
        assert keys[2] == '/charlie'

        # compare with original
        original_paths = original_openapi_json.get('paths')
        assert len(paths) == len(original_paths)
        for path, value in paths.items():
            original_path = [v for k, v in original_paths.items() if path == k]
            assert original_path
            assert value == original_path[0]

    @classmethod
    def assert_others(cls, openapi_json, original_openapi_json):
        for key, value in openapi_json.items():
            if key in ['paths', 'components', 'tags']:
                continue

            assert value == original_openapi_json.get(key)

    @classmethod
    def assert_component_schemas(cls, openapi_json, original_openapi_json):
        components = openapi_json.get('components')
        schemas = components.get('schemas')
        assert len(schemas) == 3

        keys = list(schemas.keys())
        assert keys[0] == 'Alpha'
        assert keys[1] == 'Bravo'
        assert keys[2] == 'Charlie'

        # compare with original
        original_schemas = original_openapi_json.get('components').get('schemas')
        assert len(schemas) == len(original_schemas)
        for key, value in schemas.items():
            original_value = [v for k, v in original_schemas.items() if key == k]
            assert original_value
            assert value == original_value[0]
        return components

    @classmethod
    def assert_component_request_bodies(cls, openapi_json, original_openapi_json):
        # requestBodies
        components = openapi_json.get('components')
        request_bodies = components.get('requestBodies')
        assert len(request_bodies) == 3

        keys = list(request_bodies.keys())
        assert keys[0] == 'AlphaBody'
        assert keys[1] == 'BravoBody'
        assert keys[2] == 'CharlieBody'

        # compare with original
        original_request_bodies = original_openapi_json.get('components').get('requestBodies')
        assert len(request_bodies) == len(original_request_bodies)
        for key, value in request_bodies.items():
            original_value = [v for k, v in original_request_bodies.items() if key == k]
            assert original_value
            assert value == original_value[0]

    @classmethod
    def assert_tags(cls, openapi_json, original_openapi_json):
        tags = openapi_json.get('tags')
        assert len(tags) == 3

        assert tags[0].get('name') == 'alpha'
        assert tags[1].get('name') == 'bravo'
        assert tags[2].get('name') == 'charlie'

        # compare with original
        original_tags = original_openapi_json.get('tags')
        assert len(tags) == len(original_tags)
        for tag in tags:
            original_tag = [v for v in original_tags if tag.get('name') == v.get('name')]
            assert original_tag
            assert tag == original_tag[0]
