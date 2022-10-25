from rsa_crypt import rsa_descrypt
import requests
import os
from creator import get_pp_from_pickle, write_to_bytes, add_pp_to_pickle
import ast

#Adding file to IPFS
def add_data_to_ipfs(file, privatk):
    with open(file, 'rb') as txt:
        text_binary = txt.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": text_binary})
        ipfs_hash = response.json()["Hash"]
        print("File has been added to IPFS")
        add_pp_to_pickle(ipfs_hash, privatk)
    os.remove(file)
    return ipfs_hash

#Geting data from IPFS
def get_data_from_ipfs(hash_ipfs, pk):
    try:
        url = f'https://ipfs.io/ipfs/{hash_ipfs}'
        answer = requests.get(url)
        crypted_text = answer.content
        descrypted_text = rsa_descrypt(crypted_text, pk)
        print("Descrypted has been succesfull")
        descrypted_dict = ast.literal_eval(descrypted_text)
        print(descrypted_dict)
        return descrypted_dict
    except Exception:
        print("Code 504. Try again...")
        get_data_from_ipfs(hash_ipfs, pk)

#Changing data in IPFS (In fact, we delete the previous file with the connection key and create a new one, then adding new to IPFS)
def change_data_in_ipfs(ipfs_hash, dict: dict):
    get_pp_from_pickle(ipfs_hash, delete=True)
    (priv_k, file) = write_to_bytes(dict)
    (hash_ipfs) = add_data_to_ipfs(file)
    add_pp_to_pickle(hash_ipfs, priv_k)
    print("Changing data in ipfs has been completed")
