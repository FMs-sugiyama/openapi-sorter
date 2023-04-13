import re
from time import sleep
from unittest import TestCase
from unittest.mock import Mock, patch

import pytest
from _pytest.python_api import raises
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

            assert re.sub(r'.[\s]{2,}', ' ', captured.err) == (
                '''usage: openapi_sorter [-h] (-o OUTPUT | --overwrite) FILE [FILE ...]
openapi_sorter: error: the following arguments are required: FILE
'''
            )

    @patch('sys.argv', ['openapi_sorter', 'input.yaml'])
    def test_main_no_output(self):
        try:
            main()
        except SystemExit:
            captured = self.capsys.readouterr()
            assert re.sub(r'.[\s]{2,}', ' ', captured.err) == (
                '''usage: openapi_sorter [-h] (-o OUTPUT | --overwrite) FILE [FILE ...]
openapi_sorter: error: one of the arguments -o/--output --overwrite is required
'''
            )

    @patch('sys.argv', ['openapi_sorter', 'input.yaml', '--overwrite', '--output', 'output.yaml'])
    def test_main_both_output(self):
        try:
            main()
        except SystemExit:
            captured = self.capsys.readouterr()

            assert re.sub(r'.[\s]{2,}', ' ', captured.err) == (
                '''usage: openapi_sorter [-h] (-o OUTPUT | --overwrite) FILE [FILE ...]
openapi_sorter: error: argument -o/--output: not allowed with argument --overwrite
'''
            )

    @patch('sys.argv', ['openapi_sorter', 'input-1.yaml', 'input-2.yaml', '-o', 'output.yaml'])
    def test_main_multiple_inputs_and_output(self):
        try:
            main()
        except SystemExit:
            captured = self.capsys.readouterr()

            assert re.sub(r'.[\s]{2,}', ' ', captured.err) == (
                '''usage: openapi_sorter [-h] (-o OUTPUT | --overwrite) FILE [FILE ...]
openapi_sorter: error: the '--output' option can only be used when processing a single input file
'''
            )

    @patch('sys.argv', ['openapi_sorter', 'input-1.yaml', 'input-2.yaml', '--overwrite'])
    @patch.object(OpenApiSorter, 'sort')
    def test_main_overwrite_multiple(self, sort: Mock):
        sort.return_value = (True, [])

        main()

        kwargs = sort.call_args.kwargs

        assert kwargs.get('input_files') == ['input-1.yaml', 'input-2.yaml']
        assert kwargs.get('is_overwrite') is True

    @patch('sys.argv', ['openapi_sorter', 'input.yaml', '--output', 'output.yaml'])
    @patch.object(OpenApiSorter, 'sort')
    def test_main_output(self, sort: Mock):
        sort.return_value = (True, [])

        main()

        kwargs = sort.call_args.kwargs

        assert kwargs.get('input_files') == ['input.yaml']
        assert kwargs.get('output_file') == 'output.yaml'

        # if error happen, system exit
        sort.return_value = (False, ['error message(1)', 'error message(2)'])

        with raises(SystemExit):
            main()

        captured = self.capsys.readouterr()

        assert (
            captured.out
            == '''error message(1)
error message(2)
'''
        )

    @patch('sys.argv', ['openapi_sorter', 'input.yaml', '--overwrite'])
    @patch.object(OpenApiSorter, 'sort')
    def test_main_overwrite(self, sort: Mock):
        sort.return_value = (True, [])

        main()

        kwargs = sort.call_args.kwargs

        assert kwargs.get('input_files') == ['input.yaml']
        assert kwargs.get('is_overwrite') is True

        # if error happen, system exit
        sort.return_value = (False, ['error message(1)', 'error message(2)'])

        with raises(SystemExit):
            main()

        captured = self.capsys.readouterr()

        assert (
            captured.out
            == '''error message(1)
error message(2)
'''
        )
