import random
import string
from dataclasses import dataclass


@dataclass
class Segment_Data:
    segment_name_create: str = None
    segment_name_delete: str = None


class Builder:

    @staticmethod
    def create_segment_name():
        return Segment_Data(segment_name_create=''.join(random.choices(string.ascii_letters, k=10)),
                            segment_name_delete=''.join(random.choices(string.ascii_letters, k=10)))
