import requests
import hashlib
import os
import base64

IMAGE_RESPONSE_FORMAT = {
    'image/png': 'png',
    'image/jpg': 'jpg',
    'image/jpeg': 'jpg',
}


class PICVT():
    _config = None
    _dir = "./picvt_temp"
    _basen = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        pass

    def _get_image_default(self, url):
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(e, end=' ')
            return None, None
        image = response.content
        image_format = IMAGE_RESPONSE_FORMAT[response.headers['Content-Type']] \
            if 'Content-Type' in response.headers.keys() \
            else None
        return image, image_format

    def _save_image_default(self, image, path):
        if not image:
            return False
        if os.path.exists(path):
            return False
        with open(path, 'wb') as fb:
            fb.write(image)
            fb.close()
        return True

    def _get_save_path(self, image_name):
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)
        path = os.path.join(self._dir, image_name)
        return path

    def _get_file_base64(self, file):
        data = None
        with open(file, 'rb') as f:
            data = self._get_content_base64(f.read())
            f.close()
        return data

    def _get_file_content(self, file):
        data = None
        with open(file, 'rb') as f:
            data = f.read()
            f.close()
        return data

    def _get_content_base64(self, content):
        data = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        return data

    def _get_file_format(self, filename):
        return os.path.splitext(filename)[-1]

    def _get_file_name(self, filename):
        return os.path.basename(filename)

    def _get_file_purename(self, filename):
        return "{}".format(self._get_file_name(filename))

    def _get_dict_value(self, dict, key, default=""):
        if key in dict:
            return dict[key]
        return default

    def _get_basen_encode(self, number10):
        alphabet = self._basen
        if (number10 == 0):
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while number10:
            rem = number10 % base
            number10 = number10 // base
            arr.append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)

    def _get_basen_decode(self, number62):
        alphabet = self._basen
        base = len(alphabet)
        strlen = len(number62)
        number10 = 0
        idx = 0
        for char in number62:
            power = (strlen - (idx + 1))
            number10 += alphabet.index(char) * (base ** power)
            idx += 1
        return number10

    def _get_file_md5(self, filename):
        md5 = None
        with open(filename, 'rb') as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            md5 = md5.hexdigest()
        return md5

    def _get_content_md5(self, content):
        md5 = None
        md5 = hashlib.md5()
        md5.update(content)
        md5 = md5.hexdigest()
        return md5

    def extract(self, content):
        return None

    def download(self, url):
        image, image_format = self._get_image_default(url)

        if not image or not image_format:
            return False, None

        md5 = self._get_content_md5(image)
        short_code = self._get_basen_encode(int(md5[0:8], 16))
        path = self._get_save_path("{}.{}".format(short_code, image_format))
        save_ok = self._save_image_default(image, path)

        while not save_ok and os.path.exists(path):
            save_ok = True
            exists_md5 = self._get_file_md5(path)
            if (exists_md5 != md5):
                short_code = self._get_basen_encode(self._get_basen_decode(short_code) + 1)
                path = self._get_save_path("{}.{}".format(short_code, image_format))
                save_ok = self._save_image_default(image, path)

        return save_ok, path

    def upload(self, path, params):
        return False, None
