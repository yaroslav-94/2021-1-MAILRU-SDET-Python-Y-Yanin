import pytest

from hw_3.api.client_segment import NoSuchSegmentExist
from hw_3.test_api.base import ApiBase


class TestApi(ApiBase):

    @pytest.mark.api
    def test_create(self):
        self.segment_api.create_segment(name=self.segment_api.segment_names.segment_name_create)

        self.segment_api.is_segment_exists(name=self.segment_api.segment_names.segment_name_create)

        self.segment_api.delete_segment(id_segment=self.segment_api.segment_id)

    @pytest.mark.api
    def test_delete(self):
        self.segment_api.create_segment(name=self.segment_api.segment_names.segment_name_delete)

        self.segment_api.delete_segment(id_segment=self.segment_api.segment_id)

        with pytest.raises(NoSuchSegmentExist):
            self.segment_api.is_segment_exists(name=self.segment_api.segment_names.segment_name_delete)
