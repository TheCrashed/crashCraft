import hashlib
import urllib2

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto import Random


def generate_key_pair():
	return RSA.generate(1024)

def generate_bytes(bytes=4):
	return Random.get_random_bytes(bytes)

def generate_server_id(bytes=20):
	return ''.join('%02x' % ord(c) for c in generate_bytes(bytes))

def encrypt(key, message):
	cipher = PKCS1_v1_5.new(key)
	return cipher.encrypt(message)

def decrypt(key, message):
	cipher = PKCS1_v1_5.new(key)
	return cipher.decrypt(message, None)

def java_hex_digest(digest):
	d = long(digest.hexdigest(), 16)
	if d >> 39*4 & 0x8:
		d = "-%x" % ((-d) & (2**(40*4)-1))
	else:
		d = "%x" % d
	return d

def cipher(key):
	return AES.new(key, AES.MODE_CFB, key, segment_size=8)

def validate_client(server_id, shared_secret, public_key, username):
	sha1 = hashlib.sha1()
	sha1.update(server_id)
	sha1.update(shared_secret)
	sha1.update(public_key)
	digest = java_hex_digest(sha1)

	try:
		value = urllib2.urlopen('http://session.minecraft.net/game/checkserver.jsp?user=%s&serverId=%s' % (username, digest)).read()
		if value == 'YES':
			return True
	except:
		pass
