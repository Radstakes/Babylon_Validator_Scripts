# Radix Babylon Validator Scripts

This repository provides a number of tools to assist validators on the Radix network.  The validator owner badge is used for authorisation to call certain methods on the validator component, such as register, unregister and update_key.  The following scripts use the Radix Engine Toolkit for constructing and signing transactions programatically.  The validators Keystore.ks file is used as the wallet for signing transactions so the badge is required to be transferred to this wallet.

*Warning - the owner badge has absolute control of the validator component, so you should be comfortable transferring the badge to the Keystore wallet and ensure that you have a strong password to protect it.  It is always possible to transfer the owner badge back to another address (for example, one which is connected to your mobile wallet) and a script is provided here to do so.

Pre-requisites:
You must install the Radix Engine Tookit plus the dependencies listed in the scripts where required:

1. Run `pip3 install radix-engine-toolkit`

### Mainnet_Validator_Keystore_Address.py
This Python script reads a node-keystore.ks file, requests the password and then derives the Babylon wallet address which is associated with the public key.  This address is required for the 'unregister', 'register' and 'update key' scripts which follow and will the address you send the owner badge to.

1. Run `python3 Mainnet_Validator_Keystore_Address.py`
2. Enter Keystore password when prompted
   
### Mainnet_Move_Owner_Badge.py
This Python script reads the node-keystore.ks file, derives the account and compiles a transaction manifest which will send the validator owner badge from the address associated with the keystore, to an alternate address.  This is required if you want to bring the badge back to a wallet you control through the mobile wallet for example.

The script will request your Keystore password, compile a manifest, then request confirmation of the first epoch that the tx is valid.  The manifest will then be submitted to the Radix Gateway before waiting 5 seconds before querying the transaction status.

1. Edit the script with the `DESTINATION_ACCOUNT` which is where you would like to deposit the owner badge to (normally an address of the mobile wallet)

2. Run `python3 Mainnet_Move_Owner_Badge.py`

2. Enter your Keystore password when prompted
3. Review the manifest to ensure it is as expected
4. Enter the current epoch when prompted

### Unregister
