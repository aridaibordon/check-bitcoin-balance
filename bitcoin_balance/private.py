import ecdsa
import hashlib
import base58

def get_public_address_from_private_key(private_key: str):
    """ Return the public address from a private key

    Parameters
    ----------
    * private_key: string with the private key.

    Original code from Shlomi Zeltsinger (https://www.youtube.com/watch?v=tX-XokHf_nI).

    ALWAYS REMEMBER TO KEEP YOUR PRIVATE KEYS SECRET. THE ACCESS OF A THIRD PARTY TO YOUR
    KEYS COULD LEAD TO THE LOSE OF ALL YOUR FUNDS.

    """
    # WIF to private key by https://en.bitcoin.it/wiki/Wallet_import_format
    private_key = base58.b58decode_check(private_key) 
    private_key = private_key[1:]

    # Private key to public key (ecdsa transformation)
    signing_key = ecdsa.SigningKey.from_string(private_key, curve = ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key = bytes.fromhex("04") + verifying_key.to_string()

    # hash sha 256 of pubkey
    sha256_1 = hashlib.sha256(public_key)

    # hash ripemd of sha of pubkey
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(sha256_1.digest())

    # checksum
    hashed_public_key = bytes.fromhex("00") + ripemd160.digest()
    checksum_full = hashlib.sha256(hashlib.sha256(hashed_public_key).digest()).digest()
    checksum = checksum_full[:4]
    bin_addr = hashed_public_key + checksum

    # encode address to base58 and print
    public_address = base58.b58encode(bin_addr)
    return public_address.decode("utf-8")