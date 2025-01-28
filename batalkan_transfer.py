from web3 import Web3

rpc_url = "https://assam-rpc.tea.xyz" 

web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    raise Exception("Gagal terhubung ke jaringan")


sender_address = ""
private_key = ""


nonce = web3.eth.get_transaction_count(sender_address, "pending")

cancel_tx = {
    "chainId": 93384,
    "gas": 21000, 
    "gasPrice": web3.to_wei("30", "gwei"),
    "nonce": nonce,  
    "to": sender_address,  
    "value": 0, 
}


signed_cancel_tx = web3.eth.account.sign_transaction(cancel_tx, private_key)


cancel_tx_hash = web3.eth.send_raw_transaction(signed_cancel_tx.raw_transaction)


cancel_tx_receipt = web3.eth.wait_for_transaction_receipt(cancel_tx_hash)


print(f"Transaksi pembatalan berhasil! Hash: {web3.to_hex(cancel_tx_hash)}")
print(f"Detail transaksi: {cancel_tx_receipt}")
