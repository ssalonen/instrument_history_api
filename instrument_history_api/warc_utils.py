from gzip import GzipFile
from io import BytesIO
from warcat.util import parse_http_response
from requests import Request
from requests.adapters import HTTPAdapter

_DUMMY_ADAPTER = HTTPAdapter()

def text_content_from_record(record):
    url = record.header.fields['WARC-Target-URI']
    request = Request()
    request.url = url

    file_obj = record.content_block.binary_block.get_file()
    data = file_obj.read(record.content_block.binary_block.length)
    resp = parse_http_response(data)
    
    # Use requests heuristics to determine encoding
    encoding = _DUMMY_ADAPTER.build_response(request, resp).encoding
    uncompressed_data = (GzipFile(fileobj=resp.fp) if resp.headers.get('Content-Encoding') == 'gzip' else resp.fp).read()
    return uncompressed_data.decode(encoding or 'utf-8', errors='replace')
    

def filter_response_records(records):
    return (record
        for record in records
            if record.header.fields['WARC-type'] == 'response' and
               record.content_block.fields.status_code == 200)
