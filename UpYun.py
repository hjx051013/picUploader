import requests
from io import BytesIO
import upyun
from CommonYun import CommonYun


class Upai(CommonYun):
    def __init__(self, servicename, operatorname, password, domain):
        self.option = "upai"
        CommonYun.__init__(self, domain)
        self.up = upyun.UpYun(servicename, operatorname, password)

    def upload_file(self, upload_file_name, key, is_old_link):
        res = None
        if is_old_link:
            response = requests.get(upload_file_name)
            if response.status_code == 200:
                file = BytesIO(response.content)
                res = self.up.put(key, file, checksum=True)
        else:
            with open(upload_file_name, 'rb') as f:
                res = self.up.put(key, f, checksum=True)

        return self.domain + "/" + key if res else None



