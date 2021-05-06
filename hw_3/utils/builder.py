import random
import string


class Builder:

    @staticmethod
    def create_segment_name(name=""):
        return str(name)+" "+''.join(random.choices(string.ascii_letters, k=10))
