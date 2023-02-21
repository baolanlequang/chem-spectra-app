from flask import request
def build_file_convert_request(receivedRequest: request = None):
  if receivedRequest is None:
    return None
  return ""