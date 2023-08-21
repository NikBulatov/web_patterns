class Route:
    def __init__(self, routes, path):
        self.routes = routes
        self.url = path

    def __call__(self, view):
        self.routes[self.url] = view()
