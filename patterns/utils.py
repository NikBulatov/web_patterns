from time import time


class SingletonLogger(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonLogger):
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def log(text: str) -> None:
        print("LOG --->", text)


class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f"debug --> {self.name} executed {delta:2.2f} ms")
                return result

            return timed

        return timeit(cls)


class Route:
    def __init__(self, routes, path):
        self.routes = routes
        self.url = path

    def __call__(self, view):
        self.routes[self.url] = view()
