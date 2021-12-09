

def admin():
    status = '200 OK'
    response_type = [('Content-Type', 'text/html')]
    response = [b"Admin page"]
    return status, response_type, response
