from chem_spectra.helper.request import build_file_convert_request
from flask import ( request )

def test_non_request():
  convert_request = build_file_convert_request(None)
  assert convert_request is None

def test_invalid_request():
  convert_request = build_file_convert_request("just a string")
  assert convert_request is None

# def test_valid_request():
#   convert_request = build_file_convert_request()
#   assert convert_request is request
