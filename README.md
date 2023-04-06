How to use?


1. Install IPFS (or kubo) in your computer with this repo.
2. pip install -r requirements.txt
3. Before use run "ipfs_daemon.bat", or if you work in Linux, etc. write in terminal "ipfs daemon"

Decentralized database solution on IPFS.

This project is my decentralized database solution. As the main place where the information will be stored, I chose the IPFS peer-to-peer communication protocol.
Unlike most databases, this database does not have a tabular form. It takes a dictionary and returns that too (although if you edit the script, you can store almost any type of information). I recommend saving the information in the format "1 object (with its description) - 1 node (on which information is stored in IPFS)". Hashes that are returned when added to IPFS can already be tied to specific things. Nodes can be manipulated using the functions that I wrote in the scripts.
There was also the problem of easy access to data on IPFS - they are stored there, in fact, in the public domain, and there is a risk that some third party can brute force the hash, which, in fact, is the address to the data on IPFS. Therefore, in my system, before sending information to IPFS, it is additionally encrypted with RSA. After that, the data is sent to IPFS in encrypted form, and the file with a hash remains in the system, which contains a private key with a unique data type, thanks to which we can request this data back to the system.
It is possible that third person can try to access the data if he first get access to the system where the IPFS hashes with private keys are located, so at this stage I recommend storing these files on different hosts and reconfiguring the connection to them in order to diversify the damage.

Data remains on IPFS forever - you need to come to terms with this. Therefore, the “change_data_in_ipfs()” function only imitates the replacement of information in the database - in fact, a new node is created, to which the information is sent and remains stored there in encrypted form. Therefore, by the way, you do not need to worry about the safety of your previous data, because the keys to them are deleted, and they themselves are encrypted, and it is unlikely that they will ever be found and decrypted.
Perhaps I will update this repository, and even come up with a proper name for it! In the meantime, good luck to everyone, use your health.
