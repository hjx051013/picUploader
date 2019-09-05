from qiniu import Auth, put_file, etag, BucketManager
from CommonYun import CommonYun


class Qiniu(CommonYun):
    def __init__(self, accesskey, secretkey, bucketname, domain):
        self.option = "qiniu"
        self.bucketname = bucketname
        CommonYun.__init__(self, domain)
        self.qiniu = Auth(accesskey, secretkey)  # 七牛认证
        self.Bucket_Manager = BucketManager(self.qiniu)  # 初始化BucketManager

    def upload_file(self, upload_file_name, key, is_old_link):
        if is_old_link:
            ret, info = self.Bucket_Manager.fetch(upload_file_name, self.bucketname, key)
            if ret['key'] == key:
                return self.domain + '/' + key
        else:
            mime_type = upload_file_name[upload_file_name.rfind('.') + 1:]
            token = self.qiniu.upload_token(self.bucketname, key)
            ret, info = put_file(token, key, upload_file_name, mime_type=mime_type, check_crc=True)
            if ret['key'] == key and ret['hash'] == etag(upload_file_name):
                return self.domain + '/' + key


