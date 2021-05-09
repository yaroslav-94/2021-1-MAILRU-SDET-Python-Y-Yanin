from hw_3.api.client_base import ApiClient


class NoSuchSegmentExist(Exception):
    pass


class ApiClientSegment(ApiClient):

    def __init__(self, base_url):
        super().__init__(base_url)

        self.segment_id = None

    def create_segment(self, name):
        location_segment = "api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags"

        data_segment = {
            "logicType": "or",
            "name": f"{name}",
            "pass_condition": 1,
            "relations": [
                {"object_type": "remarketing_player", "params": {"type": "positive", "left": 365, "right": 0}}]
        }

        headers_segment = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "X-CSRFToken": f"{self.csrf_token}"
        }

        responce_segment = self._request(method="POST", location=location_segment, json=data_segment,
                                         headers=headers_segment)
        self.segment_id = responce_segment.json()["id"]

    def delete_segment(self, id_segment):
        location_delete = "api/v1/remarketing/mass_action/delete.json"

        headers_delete = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "X-CSRFToken": f"{self.csrf_token}"
        }

        data_delete = [{"source_id": f"{id_segment}", "source_type": "segment"}]

        self._request(method="POST", location=location_delete, headers=headers_delete, json=data_delete)

    def is_segment_exists(self, name):
        is_exist = False
        location_segment = "api/v2/remarketing/segments.json?fields=id,name"

        headers_segment = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru",
            "Connection": "keep-alive",
            "X-CSRFToken": self.csrf_token
        }

        response_exist = self._request(method="GET", location=location_segment, headers=headers_segment)

        for value in response_exist.json()['items']:
            if value['name'] == name:
                is_exist = True

        if not is_exist:
            raise NoSuchSegmentExist(f"Segment with name {name} not created")
