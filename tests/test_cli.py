from unittest import TestCase
from unittest.mock import Mock, patch

import pytest
from openapi_sorter.cli import main
from openapi_sorter.openapi_sorter import OpenApiSorter


class TestCli(TestCase):
    @pytest.fixture(autouse=True)
    def _pass_capsys(self, capsys):
        self.capsys = capsys

    @pytest.fixture(autouse=True)
    def _pass_monkeypatch(self, monkeypatch):
        self.monkeypatch = monkeypatch

    @patch('sys.argv', ['openapi_sorter'])
    def test_main_no_input(self):
        try:
            main()
        except SystemExit:
            captured = self.capsys.readouterr()
            assert captured.err == (
                'usage: openapi_sorter [-h] (-o OUTPUT | --overwrite) input'
                '\n'
                'openapi_sorter: error: the following arguments are required: input'
                '\n'
            )

    @patch('sys.argv', ['openapi_sorter', 'input.yaml'])
    def test_main_no_output(self):
        try:
            main()
        except SystemExit:
            captured = self.capsys.readouterr()
            assert captured.err == (
                'usage: openapi_sorter [-h] (-o OUTPUT | --overwrite) input'
                '\n'
                'openapi_sorter: error: one of the arguments -o/--output --overwrite is required'
                '\n'
            )

    @patch('sys.argv', ['openapi_sorter', 'input.yaml', '--overwrite', '--output', 'output.yaml'])
    def test_main_both_output(self):
        try:
            main()
        except SystemExit:
            captured = self.capsys.readouterr()
            assert captured.err == (
                'usage: openapi_sorter [-h] (-o OUTPUT | --overwrite) input'
                '\n'
                'openapi_sorter: error: argument -o/--output: not allowed with argument --overwrite'
                '\n'
            )

    @patch('sys.argv', ['openapi_sorter', 'input.yaml', '--output', 'output.yaml'])
    @patch.object(OpenApiSorter, 'sort')
    def test_main_output(self, sort: Mock):
        main()

        kwargs = sort.call_args.kwargs

        assert kwargs.get('input_file') == 'input.yaml'
        assert kwargs.get('output_file') == 'output.yaml'

    @patch('sys.argv', ['openapi_sorter', 'input.yaml', '--overwrite'])
    @patch.object(OpenApiSorter, 'sort')
    def test_main_overwrite(self, sort: Mock):
        main()

        kwargs = sort.call_args.kwargs

        assert kwargs.get('input_file') == 'input.yaml'
        assert kwargs.get('is_overwrite') is True
