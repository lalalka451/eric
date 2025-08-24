import uuid

def get_session_id():
    session_id = str(uuid.uuid4())
    return session_id


def get_jobsdb_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Seek-Ec-Sessionid': get_session_id(),
    }
    return headers

def get_jobsdb_headers_with_session(session_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Seek-Ec-Sessionid': session_id,
    }
    return headers