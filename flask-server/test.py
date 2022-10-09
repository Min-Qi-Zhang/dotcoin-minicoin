from nacl.signing import SigningKey
from nacl.encoding import HexEncoder, RawEncoder
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import pickle

data_to_sign = 'hello worldd'
private_key_location = './private_key'

# generate private key
# private_key = SigningKey.generate()
# f = open(private_key_location, 'wb')
# pickle.dump(private_key, f)
# f.close()

# read private key from file
f = open(private_key_location, 'rb')
private_key = pickle.load(f)
f.close()

# get public key
public_key = private_key.verify_key.encode(encoder=RawEncoder)
# print(public_key)
public_key = bytes.hex(public_key)

print(public_key)
print(len(public_key))
# print(bytes.fromhex(public_key))
# exit()

# sign
signed_hex = private_key.sign(data_to_sign.encode('utf-8'), encoder=RawEncoder)
signature_bytes = RawEncoder.decode(signed_hex.signature)
signature = bytes.hex(signature_bytes)

# verify
verify_key = VerifyKey(bytes.fromhex(public_key), encoder=RawEncoder)
# signature_bytes = bytes.fromhex(signature)
try:
    # print(len(data_to_sign.encode('utf-8')))
    # print(len(bytes.fromhex(signature)))
    verify_key.verify(data_to_sign.encode('utf-8'), bytes.fromhex(signature), encoder=RawEncoder)
    print ("The message is authentic.")
except BadSignatureError:
    print ("The message is not authentic.")