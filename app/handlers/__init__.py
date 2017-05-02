def parse_error_response(e):
  message = '%s: %s' % \
    (e.data['message'].values()[0], \
     e.data['message'].keys()[0])
  return error_response(message, 400)


def error_response(message, code):
  return dict(
    status='error',
    message=message,
  ), code


def ok_response(message=None, data=None, code=200):
  _ret = dict(
    status='ok',
  )
  if message:
    _ret['message'] = message
  if data:
    _ret['data'] = data

  return _ret, code