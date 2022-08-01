import time
import requests

# seconds (multiplies by 3 for POST endpoints)
MIN_TIME_BETWEEN_REQUESTS = 2


class Maps():

    API_URL = 'https://cartes.io/api/'
    API_KEY = None
    LAST_REQUEST_TIME = 0

    def __init__(self, map_uuid=None, api_key=None, map_token=None):

        self.map_uuid = map_uuid

        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = self.API_KEY

        self.map_token = map_token

        self.request = None

        self.headers = {'Content-type': 'application/json',
                        'Accept': 'application/json'}

        self.params = {'map_token': self.map_token,
                       'api_key': self.api_key}

        if (not self.request):
            self.request = self.API_URL+'maps'
            if self.map_uuid is not None:
                self.request += '/{}'.format(self.map_uuid)

    def convert_to_string(self, value):
        if isinstance(value, bool):
            value = str(value).lower()
        elif isinstance(value, int) or isinstance(value, float):
            value = str(value)
        elif isinstance(value, list):
            value = ','.join(value)
        elif isinstance(value, dict):
            value = str(value)
        else:
            value = str(value)
        return value

    def add_param(self, key, value):
        # Convert value to a string value for URL
        self.params[key] = self.convert_to_string(value)
        return self

    def add_header(self, key, value):
        self.headers[key] = value
        return self

    def page(self, page_number):
        self.params['page'] = page_number
        return self

    def markers(self, marker_id=None):
        # Get the markers
        self.request = self.API_URL+'maps/{}/markers'.format(
            self.map_uuid)
        if marker_id is not None:
            self.request += '/{}'.format(marker_id)
        return self

    def related(self):
        # Get the markers
        self.request = self.API_URL+'maps/{}/related'.format(
            self.map_uuid)
        return self

    def wait_for_limiter(self, method='GET'):
        min_time = (MIN_TIME_BETWEEN_REQUESTS if method ==
                    'GET' else MIN_TIME_BETWEEN_REQUESTS*3)
        if (time.time() - self.LAST_REQUEST_TIME) < min_time:
            time.sleep(min_time)
        return self

    def handle_request(self, method="get", data=None):

        self.attach_params_to_url()

        # If not enough time has passed since the last request, wait
        self.wait_for_limiter(method.upper())

        try:
            response = requests.request(
                method.lower(), self.request, json=data, headers=self.headers)

            self.LAST_REQUEST_TIME = time.time()

            return self.handle_response(response)
        except Exception as e:
            print(e)

    def get(self):

        return self.handle_request()

    def create(self, data):

        return self.handle_request('post', data)

    def update(self, data):

        return self.handle_request('put', data)

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            print('Error: {}'.format(response.status_code))
            # print message
            print(response.json())

    def attach_params_to_url(self):
        # this is another way of serializing the URL
        preq = requests.PreparedRequest()
        preq.prepare_url(self.request, self.params)
        self.request = preq.url
        return self
