from web3 import Web3
from rich import print
from rich.progress import Progress
import random
import time


rpc_url = "https://assam-rpc.tea.xyz" 
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    raise Exception("Gagal terhubung ke jaringan")

sender_address = ""  
private_key = ""  

contract_address = "" 

contract_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]


contract = web3.eth.contract(address=contract_address, abi=contract_abi)


with open("addresses.txt", "r") as file:
    addresses = file.read().splitlines()


success_count = 0
failed_count = 0

with Progress() as progress:
    task = progress.add_task("[cyan]Mengirim token...", total=len(addresses))

    for recipient_address in addresses:
        try:
            amount = random.randint(100, 1000)  # Jumlah token acak
            amount_wei = web3.to_wei(amount, "ether")

            nonce = web3.eth.get_transaction_count(sender_address)
            tx = contract.functions.transfer(recipient_address, amount_wei).build_transaction({
                "chainId": 93384,
                "gas": 2000000,
                "gasPrice": web3.to_wei("30", "gwei"), 
                "nonce": nonce,
            })

            signed_tx = web3.eth.account.sign_transaction(tx, private_key)

            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            print(f"[green]✔ Berhasil[/green] Mengirim {amount} token ke {recipient_address}")
            print(f"  - Hash Transaksi: {web3.to_hex(tx_hash)}")
            print(f"  - Block: {tx_receipt['blockNumber']}")
            print(f"  - Gas Used: {tx_receipt['gasUsed']}")
            success_count += 1
        except Exception as e:
            print(f"[red]✘ Gagal[/red] Mengirim ke {recipient_address}: {e}")
            failed_count += 1

        progress.update(task, advance=1)

        sleep_time = random.uniform(1, 6)
        time.sleep(sleep_time)

print("\n[bold]Ringkasan Transfer:[/bold]")
print(f"  - Total Alamat: {len(addresses)}")
print(f"  - Berhasil: {success_count}")
print(f"  - Gagal: {failed_count}")
