# Custom exception class
class SampleSizeError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Function that raises the custom exception

