import json
import requests

QUERY=""
HOST = "http://localhost:5000"
PATH =  "/rest/firmware/"

#curl 'http://localhost:5000/rest/firmware/e692eca8505b0f4a3572d4d42940c6d5706b8aabec6ad1914bd4d733be9dfecf_25221120' -X GET

def _make_get_requests(url):
    response = requests.get(url)
    response_data=response.text
    response_dict=json.loads(response_data)
    return response_dict

firmware_data =_make_get_requests("http://localhost:5000/rest/firmware/b7c55a6de9fd1b85ec07f661b4d21638021999e2b1e754de1922f3b01f2cedb8_3378139")
meta_data = firmware_data['firmware']['meta_data']
analysis = firmware_data['firmware']['analysis']
pass