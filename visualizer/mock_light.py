class MockLight:
    """In-memory stand-in for light.Light — same set_state / get_state surface."""

    def __init__(self):
        self.state = None

    def get_state(self):
        return self.state

    def set_state(self, state, seriously=False):
        self.state = state
