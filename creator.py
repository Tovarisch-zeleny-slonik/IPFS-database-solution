from rsa_crypt import rsa_encrypt
from interaction_with_ipfs import *
import pickle

#ATTENTION! Before you input dict, be sure to check the indents!!! (Example: {"mario": 2, "sergo": "vanila"})
def write_to_bytes(dict: dict):
    file = 'buffer.bin'
    with open(file, 'wb') as db:
        content, pk = rsa_encrypt(dict)
        db.write(content)
    print("File has been completed")
    return pk, file

#Saving keys under hash name in "pickles" folder
def add_pp_to_pickle(ipfs_hash, pp):
    with open(f'pickles/{ipfs_hash}', 'wb') as f:
        pickle.dump(pp, f)
    print("PP was loaded on serv")

#Extracting the private key by its hash in the "pickles" folder
def get_pp_from_pickle(hash_ipfs, delete=False):
    if delete is True:
        os.remove(f"./pickles/{hash_ipfs}")
    else:
        with open(f"./pickles/{hash_ipfs}", "rb") as g:
            pz = pickle.load(g)
        print("Private key was executed")
        return pz

if __name__ == '__main__':
    privk, file = write_to_bytes({"blah-blah-blah": "blah-blah-blah"}) #Input your dict!
    hash_ipfs = add_data_to_ipfs(file, privk)
    pk = get_pp_from_pickle(hash_ipfs)
    get_data_from_ipfs(hash_ipfs, pk)
