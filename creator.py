import pickle
import requests
import os
import ast
import rsa


class IPFS_Database:
    #ATTENTION! Before you input dict, be sure to check the indents!!! (Example: {"mario": 2, "sergo": "vanila"})
    @classmethod
    def write_to_bytes(self, dict: dict):
        self.file = 'buffer.bin'
        with open(self.file, 'wb') as db:
            content, pk = self.__rsa_encrypt(dict)
            db.write(content)
        print("File has been completed")
        return pk

    #Add data to IPFS
    def add_data_to_ipfs(self, privatk):
        with open(self.file, 'rb') as txt:
            text_binary = txt.read()
            ipfs_url = "http://127.0.0.1:5001"
            endpoint = "/api/v0/add"
            response = requests.post(ipfs_url + endpoint, files={"file": text_binary})
            ipfs_hash = response.json()["Hash"]
            print("File has been added to IPFS")
            self._add_pp_to_pickle(ipfs_hash, privatk)
        os.remove(self.file)
        return ipfs_hash

    #Geting data from IPFS
    def get_data_from_ipfs(self, hash_ipfs, pk):
        try:
            url = f'https://ipfs.io/ipfs/{hash_ipfs}'
            answer = requests.get(url)
            crypted_text = answer.content
            descrypted_text = self.__rsa_descrypt(crypted_text, pk)
            print("Descryption has been succesfull")
            descrypted_dict = ast.literal_eval(descrypted_text)
            return descrypted_dict
        except Exception:
            print("Code 504. Try again...")
            self.get_data_from_ipfs(hash_ipfs, pk)

    #Changing data in IPFS (In fact, we delete the previous file with the connection key and create a new one, then adding new to IPFS)
    def change_data_in_ipfs(self, ipfs_hash, dict: dict):
        self._get_pk_from_pickle(ipfs_hash, delete=True)
        (priv_k, file) = self.write_to_bytes(dict)
        (hash_ipfs) = self.add_data_to_ipfs(file)
        self._add_pp_to_pickle(hash_ipfs, priv_k)
        print("Changing data in ipfs has been completed")

    #Saving keys under hash name in "pickles" folder
    @classmethod
    def _add_pp_to_pickle(cls, ipfs_hash, pp):
        folder = os.listdir()
        i = "pickles"
        if i in folder:
            with open(f'pickles/{ipfs_hash}', 'wb') as f:
                pickle.dump(pp, f)
        else:
            os.mkdir("pickles")
            with open(f'pickles/{ipfs_hash}', 'wb') as f:
                pickle.dump(pp, f)
        print("Private key was loaded in file 'pickles'")

    #Extracting the private key by its hash in the "pickles" folder
    @classmethod
    def _get_pk_from_pickle(cls, hash_ipfs, delete=False):
        if delete is True:
            os.remove(f"./pickles/{hash_ipfs}")
        else:
            with open(f"./pickles/{hash_ipfs}", "rb") as g:
                pk = pickle.load(g)
            print("Private key was executed")
            return pk
    
    #Encrypting informatinon before sending to IPFS
    @staticmethod
    def __rsa_encrypt(text1):
        (public_key, private_key) = rsa.newkeys(2048)
        new_str = str(text1)
        text2 = new_str.encode('utf-8')
        crypto = rsa.encrypt(text2, public_key)
        return crypto, private_key

    #Descrypting information after response from IPFS
    @staticmethod
    def __rsa_descrypt(text, pk):
        text = rsa.decrypt(text, pk)
        cont = text.decode('utf-8')
        return cont

if __name__ == '__main__':
    ddb = IPFS_Database()
    privk = ddb.write_to_bytes({"Mark Lukan": 60, "Vizimir Zalas": 11}) #Input your dict!
    hash_ipfs = ddb.add_data_to_ipfs(privk)
    pk = ddb._get_pk_from_pickle(hash_ipfs)
    text = ddb.get_data_from_ipfs(hash_ipfs, pk)
    print(text)

