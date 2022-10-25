import rsa

#Encrypting informatinon before sending to IPFS
def rsa_encrypt(stroa):
    (public_key, private_key) = rsa.newkeys(2048)
    new_str = str(stroa)
    text = new_str.encode('utf-8')
    crypto = rsa.encrypt(text, public_key)
    return crypto, private_key

#Descrypting information after response from IPFS
def rsa_descrypt(stra, pk):
    text = rsa.decrypt(stra, pk)
    cont = text.decode('utf-8')
    return cont
