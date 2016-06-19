
class topic:
    def __init__(self, topic):
        self.topic = topic

    def __call__(self, f):
        def wrapper(*args):
            if args[1] == self.topic:
                return f(*args)
        return wrapper