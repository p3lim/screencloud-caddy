import ntpath
import time, calendar
import hmac, hashlib, base64
import string, random

import requests

class SignatureAuth(requests.auth.AuthBase):
	def __init__(self, key, secret):
		self.AUTH_HEADER = 'Signature keyId="{0}",algorithm="hmac-sha256",headers="timestamp token",signature="{1}"'

		self.key = key
		self.secret = secret.encode('utf-8')
		self.token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)).encode('utf-8')

	def __call__(self, request):
		timestamp = str(calendar.timegm(time.gmtime())).encode('utf-8')

		digest = hmac.new(self.secret, timestamp + self.token, hashlib.sha256).digest()
		signature = base64.b64encode(digest).decode('utf-8')

		request.headers['Token'] = self.token
		request.headers['Timestamp'] = timestamp
		request.headers['Authorization'] = self.AUTH_HEADER.format(self.key, signature)

		return request

def upload(url, file_path, key=None, secret=None):
	file_name = ntpath.basename(file_path)

	with open(file_path, 'rb') as file:
		files = {str(file_name): file}

		if key and secret:
			response = requests.post(url, files=files, auth=SignatureAuth(key, secret))
		else:
			response = requests.post(url, files=files)

	response.raise_for_status()

	return response.url + file_name
