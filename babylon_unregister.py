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

private_key_bytes_ret: bytes = <enter private key bytes here>

private_key_ret: PrivateKey = PrivateKey.new_ed25519(list(private_key_bytes_ret))

public_key: PublicKey = private_key_ret.public_key()

account: Address = derive_virtual_account_address_from_public_key(
        public_key, network_id
    )

def random_nonce() -> int:
    """
    Generates a random secure random number between 0 and 0xFFFFFFFF (u32::MAX)
    """
    return secrets.randbelow(0xFFFFFFFF)


SOURCE_ACCOUNT: str = (
    account.as_str()
)

print("Please ensure your Validator owner badge is in this account and there is at least 10XRD present:",SOURCE_ACCOUNT)

# The address of the validator on the Babylon network. This address will be used
# to determine the non-fungible local id of the validator owner badge.
BABYLON_VALIDATOR_ADDRESS: str = ("validator_rdx1sds4prpgf0p25pu458fg468nw9rtwqdawwg9w45hgf0t95yd3ncs09")
print("Validator Babylon Address :",BABYLON_VALIDATOR_ADDRESS)

def validator_owner_badge_non_fungible_local_id(
    validator_address: Address,
) -> NonFungibleLocalId:
    """
    Gets the non-fungible local id of owner badge associated with the given
    validator address
    """
    if validator_address.entity_type() != EntityType.GLOBAL_VALIDATOR:
        raise ValueError("The address passed is not a validator address")

    return NonFungibleLocalId.BYTES(validator_address.bytes())  # type: ignore


validator_address: Address = Address(BABYLON_VALIDATOR_ADDRESS)
owner_badge_resource_address: Address = known_addresses(
validator_address.network_id()
).resource_addresses.validator_owner_badge
owner_badge_local_id: NonFungibleLocalId = (
validator_owner_badge_non_fungible_local_id(validator_address)
)

address_book: KnownAddresses = known_addresses(network_id)
xrd_address: Address = address_book.resource_addresses.xrd
owner_badge: str = ("resource_rdx1nfxxxxxxxxxxvdrwnrxxxxxxxxx004365253834xxxxxxxxxvdrwnr")
print('\n')
manifest: TransactionManifest = (
        ManifestBuilder()
        .call_method(
            ManifestBuilderAddress.STATIC(Address(SOURCE_ACCOUNT)),
            "lock_fee",
            [ManifestBuilderValue.DECIMAL_VALUE(Decimal("10"))],
        )
        .call_method(
            ManifestBuilderAddress.STATIC(Address(SOURCE_ACCOUNT)),
            "create_proof_of_non_fungibles",
            [
                ManifestBuilderValue.ADDRESS_VALUE(
                    ManifestBuilderAddress.STATIC(Address(owner_badge))
                ),
                ManifestBuilderValue.ARRAY_VALUE(
                    ManifestBuilderValueKind.NON_FUNGIBLE_LOCAL_ID_VALUE,
                    [
                        ManifestBuilderValue.NON_FUNGIBLE_LOCAL_ID_VALUE(
                            owner_badge_local_id
                        )
                    ],
                ),
            ],
        )
       .call_method(
           ManifestBuilderAddress.STATIC(Address(BABYLON_VALIDATOR_ADDRESS)),
           "unregister", []
       )
        .build(network_id)
    )

    # Validating the manifest instructions statically, an exception is raised if
    # the manifest contains static errors.
print(manifest.instructions().as_str())

manifest.statically_validate()

urlint = "https://mainnet.radixdlt.com/statistics/validators/uptime"

headers = {"Content-Type": "application/json; charset=utf-8"}

dataint = {
  "validator_addresses": [
    BABYLON_VALIDATOR_ADDRESS
  ]
}

response = requests.post(urlint, json=dataint)
response_dict = response.json()
current_epoch = response_dict["ledger_state"]["epoch"]
end_epoch = int(current_epoch) + int(5)

print ("Start Epoch: ",current_epoch)
print ("End Epoch: ",end_epoch)

print('\n')
header: TransactionHeader = TransactionHeader(
    network_id=network_id,
    start_epoch_inclusive=current_epoch,
    end_epoch_exclusive=end_epoch,
    nonce=random_nonce(),
    notary_public_key=public_key,
    notary_is_signatory=True,
    tip_percentage=0,
)

transaction: NotarizedTransaction = (
    TransactionBuilder()
    .header(header)
    .manifest(manifest)
    .sign_with_private_key(private_key_ret)
    .notarize_with_private_key(private_key_ret)
)

# Ensure that the transaction is statically valid - if the validation fails an
# exception will be raised.
transaction.statically_validate(ValidationConfig.default(network_id))
print(f"Transaction Hash: {transaction.intent_hash().as_str()}")
print('\n')

url = "https://mainnet.radixdlt.com/transaction/submit"

headers = {"Content-Type": "application/json; charset=utf-8"}

data2 = {
     "notarized_transaction_hex": bytearray(transaction.compile()).hex()
}

response = requests.post(url, json=data2)

print("Status Code", response.status_code)

print('\n')
time.sleep(5)

urlstatus = "https://mainnet.radixdlt.com/transaction/status"

headers = {"Content-Type": "application/json; charset=utf-8"}

data3 = {
"intent_hash": transaction.intent_hash().as_str()
}

response = requests.post(urlstatus, json=data3)

print("Status Code", response.status_code)
print('\n')

response_dict = response.json()
print(json.dumps(response_dict, indent=4))
