from unittest import mock
from flask import ( request )
from chem_spectra.use_cases.convert_file import convert_single_file
from chem_spectra.helper.request import build_file_convert_request

def test_convert_single_file_without_file():
  result = convert_single_file()
  assert result is None

def test_convert_single_file_non_zip():
  repo = mock.Mock()
  
  convert_request = build_file_convert_request(request)
  result = convert_single_file(repository=repo, request=convert_request)
  assert result is not None

