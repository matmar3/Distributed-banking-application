class Endpoint(object):

    def __init__(self, host, port, route):
        self._host = host
        self._port = port
        self._route = route

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def route(self):
        return self._route
