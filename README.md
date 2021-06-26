# Multi-User Verifiable Searchable Symmetric Encryption

Semester: Spring 2021

Course: Cryptography, NTU EE

Teacher: CL Lei



## Reference Papers

- X. Liu, G. Yang, Y. Mu and R. H. Deng, "**Multi-user verifiable searchable symmetric encryption for cloud storage**," in IEEE Transactions on Dependable and Secure Computing, vol. 17, no. 6, pp. 1322-1332, 1 Nov.-Dec. 2020, doi: 10.1109/TDSC.2018.2876831.
- K. Kurosawa and Y. Ohtaki, **"UC-secure searchable symmetric encryption,"** in Proc. 16th Int. Conf. Financial Cryptography Data Secur., 2012, pp. 285–298.
- K. Kurosawa and Y. Ohtaki, **"How to update documents verifiably in searchable symmetric encryption,"** in Proc. 12th Int. Conf. Cryptology Netw. Secur., 2013, pp. 309–328.
- D. Boneh, C. Gentry, and B. Waters, **"Collusion resistant broadcast encryption with short ciphertexts and private keys,"** in Proc. 25th Annu. Int. Cryptology Conf., 2005, pp. 258–275.



## Environment

- Ubuntu 16.04 LTS
- Python 3.7.9

#### Prerequisite

- charm-crypto



## Execution

#### Setup/Store

```shell
python owner_setup_store.py
```

#### Search

```shell
bash search.sh
```

#### Modify

```shell
python owner_modify.py
```

#### Add

```shell
python owner_add.py
```

#### Delete

```shell
python owner_modify.py
```



## Report Link

