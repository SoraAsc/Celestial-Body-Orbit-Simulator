class Integrator(object):
    def __init__(self, method: str = "RK4"):
        self.method = method