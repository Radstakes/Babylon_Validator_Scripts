from radix_engine_toolkit import *
from typing import Tuple
import secrets
import requests
import json
import bech32
import ecdsa
import hashlib
import time
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from ecdsa.curves import SECP256k1
from ecdsa.util import sigencode_der
from getpass import getpass

#network id is 0x01 for mainnet, or 0x02 for Stokenet
network_id = 0x01

print ("Enter your Keystore Password:")
pw = getpass()

password = pw.encode()
print('\n')

# Read the Radix Keystore File (which is in PKCS12 format)
with open("node-keystore.ks", "rb") as f:
  private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), password, default_backend())

# Extract the unencrypted Private Key bytes
private_key_bytes = private_key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())

# Convert into Elliptic Curve Digital Signature Algorithm (ecdsa) private key object
private_key = ecdsa.SigningKey.from_der(private_key_bytes, hashfunc=hashlib.sha256)
private_key_string = private_key.to_string()

olympia_private_key = private_key_string.hex()

private_key_bytes_ret: bytes = bytes.fromhex(olympia_private_key)

# Note this is set for secp256k1 but can be changed to ed25519
private_key_ret: PrivateKey = PrivateKey.new_secp256k1(list(private_key_bytes_ret))

public_key: PublicKey = private_key_ret.public_key()

account: Address = derive_virtual_account_address_from_public_key(
        public_key, network_id
    )
print(f"Babylon Address of Keystore: {account.as_str()}")
print('\n')
