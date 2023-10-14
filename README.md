# Radix Babylon Validator Scripts

This repository provides a number of tools to assist validators on the Radix network.  The validator owner badge is used for authorisation to call certain methods on the validator component, such as register, unregister and update_key.  The following scripts use the Radix Engine Toolkit for constructing and signing transactions programatically.  The validators Keystore.ks file is used as the wallet for signing transactions so the badge is required to be transferred to this wallet.

*Warning - the owner badge has absolute control of the validator component, so you should be comfortable transferring the badge to the Keystore wallet and ensure that you have a strong password to protect it.  It is always possible to transfer the owner badge back to another address (for example, one which is connected to your mobile wallet) and a script is provided here to do so.

Pre-requisites:
You must install the Radix Engine Tookit plus the dependencies listed in the scripts where required:

1. Run `pip3 install radix-engine-toolkit`

Warning - Please ensure you understand the risks.  If your validator owner badge is sent to an address you do not have the private key for, you may lose access to it permanently!

All tools are provided free to the Radix validator community, but if you find them useful - please stake with Radstakes or drop a little donation in the owner wallet :)

### Mainnet_Validator_Keystore_Address.py
This Python script reads a node-keystore.ks file, requests the password and then derives the Babylon wallet address which is associated with the public key.  This address is required for the 'unregister', 'register' and 'update key' scripts which follow and will the address you send the owner badge to.

1. Run `python3 Mainnet_Validator_Keystore_Address.py`
2. Enter Keystore password when prompted
   
### Mainnet_Move_Owner_Badge.py
This Python script reads the node-keystore.ks file, derives the account and compiles a transaction manifest which will send the validator owner badge from the address associated with the keystore, to an alternate address.  This is required if you want to bring the badge back to a wallet you control through the mobile wallet for example.

The script will request your Keystore password, compile a manifest, then request confirmation of the first epoch that the tx is valid.  The manifest will then be submitted to the Radix Gateway before waiting 5 seconds before querying the transaction status.

1. Edit the script with the `DESTINATION_ACCOUNT` which is where you would like to deposit the owner badge to (normally an address of the mobile wallet)
2. Run `python3 Mainnet_Move_Owner_Badge.py`
3. Enter your Keystore password when prompted
4. Review the manifest to ensure it is as expected
5. Enter the current epoch when prompted

### Mainnet_Unregister.py
This Python script reads a node-keystore.ks file, requests the password and then compiles a transaction manifest to unregister a validator at the next epoch.  In order to make this transaction, the manifest will request a proof of the owner badge from the account associated with the Keystore.

1. Use the `Mainnet_Validator_Keystore_Address.py` script to derive the address associated with the Keystore.
2. Send your validator owner badge to the address from step 1.  You should also ensure there is sufficient XRD in this account as it will also be the fee payer.
3. Edit the Mainnet_Unregister.py script where the variable `BABYLON_VALIDATOR_ADDRESS` is defined and change this to your validator's address.
4. Run python3 `Mainnet_Unregister.py`
5. Enter your Keystore password when prompted
6. Review the mainfest to ensure it is as expected
7. Enter the current epoch when prompted

The transaction will then be submitted to the Gateway, and after a period of 5 seconds will query the tx hash and should display a "CommittedSuccess" message.  At the start of the next epoch, your validator will be removed from the active set.  

Note - to re-register your node, simply edit this script to change the "unregister" method to "register" in the manifest.

### Mainnet_Updatekey.py
This Python script reads a node-keystore.ks file, requests the password and then compiles a transaction manifest to update the public key associted to your validator component, at the next epoch.  In order to make this transaction, the manifest will request a proof of the owner badge from the account associated with the Keystore.

This script is particularly useful for failovers, but there are a few steps which need to be taken first.

1. If not already known, use the `Mainnet_Validator_Keystore_Address.py` script to derive the address associated with the Keystore.
2. If not already done, send your validator owner badge to the address from step 1.  You should also ensure there is sufficient XRD in this account as it will also be the fee payer.
3. In your validator default.config, config.yaml or compose file, first ensure that your primary and backup nodes have the validator address configured.  For CLI users, Docker and Systemd, this should be as follows:

Babylonnode CLI:
```core_node:
  core_release: ...
  data_directory: /home/ubuntu/babylon-ledger
  .
  .
  validator_address: <VALIDATOR_ADDRESS>```

Docker:
```RADIXDLT_CONSENSUS_VALIDATOR_ADDRESS: <VALIDATOR_ADDRESS>```

Systemd:
```consensus.validator_address=<VALIDATOR_ADDRESS>```

4. restart your nodes after updating the configs with your validator address.
5. Next you nede to obtain the public key of the node you will be wanting to failover to (normally your backup node).  You could also setup 2 scripts, one for failing over to the backup and one for failing back to the primary.  For this you just need to obtain both public keys from each node Keystore.  To obtain the public key, use the following command:

Babylonnode CLI:
```babylonnode api system identity```

Systemd/Docker:
```curl http://localhost:3334/system/identity```

6. Edit the Mainnet_Updatekey.py script where the variable `BABYLON_VALIDATOR_ADDRESS` is defined and change this to your validator's address.
7. Find the `backup_publickey` variable and update this to the public key obtained from step 5:
```backup_public_key: bytearray = bytearray.fromhex(
        "025fb0f5e60b616ceb0dffda8c76cc580b22bacc6b9bde3ca0a487b6688f332767"
    )```
8. Run python3 `Mainnet_Updatekey.py`
5. Enter your Keystore password when prompted
6. Review the mainfest to ensure it is as expected
7. Enter the current epoch when prompted

The transaction will then be submitted to the Gateway, and after a period of 5 seconds will query the tx hash and should display a "CommittedSuccess" message.  At the start of the next epoch, your primary validator will stop validating and your backup node (or whichever node's public key you specify) will now take part in consensus.  

Note - to failover back to the primary node, simply repeat step 7 with your primary node's public key and run the script again.
Warning - updating keys takes effect at the next epoch, so please ensure the changes have been made before performing any maintenance on your nodes.
