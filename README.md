# Babylon_Validator_Scripts

This repository provides a number of tools to assist validators on the Radix network.

# Mainnet_Validator_Keystore_Address.py
This Python script reads a node-keystore.ks file, requests the password and then derives the Babylon wallet address which is associated with the public key.  This address is required for the 'unregister', 'register' and 'update key' scripts which follow

# Mainnet_Move_Owner_Badge.py
This Python script reads the node-keystore.ks file, derives the account and compiles a transaction manifest which will send the validator owner badge from the address associated with the keystore, to an alternate address.  This is required if you want to bring the badge back to a wallet you control through the mobile wallet for example.

The script will request your Keystore password, compile a manifest, then request confirmation of the first epoch that the tx is valid.  Here you can simply enter the current epoch.  The manifest will then be submitted to the Radix Gateway before waiting 5 seconds before querying the transaction status.
