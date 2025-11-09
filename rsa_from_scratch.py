# Python Program for implementation of RSA Algorithm (improved)

def power(base, expo, m):
    """
    Efficient modular exponentiation (a^b mod m)
    """
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm to find gcd and coefficients
    Returns (gcd, x, y) such that ax + by = gcd
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def modInverse(e, phi):
    """
    Calculate the modular multiplicative inverse of e mod phi
    using Extended Euclidean Algorithm (more efficient)
    """
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi

# Function to calculate gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# RSA Key Generation
def generateKeys(p=7919, q=1009):
    """
    Generate RSA key pair
    
    Args:
        p, q: Prime numbers (defaults to 7919 and 1009)
        
    Returns:
        (e, d, n): Public key (e, n) and private key (d, n)
    """
    n = p * q
    phi = (p - 1) * (q - 1)

    # Common value for e
    e = 65537
    
    # Make sure e is coprime to phi(n)
    if e >= phi or gcd(e, phi) != 1:
        # Find a suitable e if 65537 doesn't work
        for candidate in range(3, phi, 2):
            if gcd(candidate, phi) == 1:
                e = candidate
                break

    # Compute d such that e * d ≡ 1 (mod phi(n))
    d = modInverse(e, phi)

    return e, d, n

# Encrypt message using public key (e, n)
def encrypt(m, e, n):
    """
    Encrypt a numeric message using RSA
    """
    return power(m, e, n)

# Decrypt message using private key (d, n)
def decrypt(c, d, n):
    """
    Decrypt a numeric message using RSA
    """
    return power(c, d, n)

# Text handling functions
def text_to_int(text):
    """
    Convert text to a single integer (for small messages only)
    """
    result = 0
    for char in text:
        result = result * 256 + ord(char)
    return result

def int_to_text(number):
    """
    Convert integer back to text
    """
    result = ""
    while number > 0:
        result = chr(number % 256) + result
        number //= 256
    return result

def encrypt_text(text, e, n):
    """
    Encrypt text message (handles one block only, small messages)
    """
    # Convert text to integer
    m = text_to_int(text)
    
    # Make sure m is less than n
    if m >= n:
        raise ValueError("Message too long for the key size")
        
    # Encrypt
    return encrypt(m, e, n)

def decrypt_text(ciphertext, d, n):
    """
    Decrypt ciphertext back to text
    """
    # Decrypt to get the numeric value
    m = decrypt(ciphertext, d, n)
    
    # Convert numeric value back to text
    return int_to_text(m)

# For larger messages, we need to break the text into blocks
def encrypt_large_text(text, e, n):
    """
    Encrypt larger text messages by breaking into blocks
    """
    # Calculate maximum bytes per block (leaving room for padding)
    byte_size = (n.bit_length() + 7) // 8 - 1
    
    # Break message into blocks
    blocks = [text[i:i+byte_size] for i in range(0, len(text), byte_size)]
    
    # Encrypt each block
    encrypted_blocks = []
    for block in blocks:
        m = text_to_int(block)
        encrypted_blocks.append(encrypt(m, e, n))
        
    return encrypted_blocks

def decrypt_large_text(encrypted_blocks, d, n):
    """
    Decrypt message that was encrypted in blocks
    """
    decrypted_text = ""
    
    for block in encrypted_blocks:
        m = decrypt(block, d, n)
        decrypted_text += int_to_text(m)
        
    return decrypted_text

# Main execution
if __name__ == "__main__":
    
    # Key Generation
    e, d, n = generateKeys()
  
    print(f"Public Key (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})")

    # Numeric message example
    M = 123
    print(f"\nOriginal Numeric Message: {M}")

    # Encrypt the message
    C = encrypt(M, e, n)
    print(f"Encrypted Message: {C}")

    # Decrypt the message
    decrypted = decrypt(C, d, n)
    print(f"Decrypted Message: {decrypted}")
    
    # Text message example (small)
    text = "Hello RSA!"
    print(f"\nOriginal Text Message: {text}")
    
    try:
        # Try to encrypt as a single block
        encrypted = encrypt_text(text, e, n)
        print(f"Encrypted (numeric): {encrypted}")
        
        # Decrypt
        decrypted_text = decrypt_text(encrypted, d, n)
        print(f"Decrypted: {decrypted_text}")
    except ValueError as ve:
        print(f"Error: {ve}")
        print("Falling back to block-based encryption")
        
        # Encrypt in blocks
        encrypted_blocks = encrypt_large_text(text, e, n)
        print(f"Encrypted blocks: {encrypted_blocks}")
        
        # Decrypt blocks
        decrypted_text = decrypt_large_text(encrypted_blocks, d, n)
        print(f"Decrypted: {decrypted_text}")
    
    # Demonstrate with larger text
    longer_text = "This is a longer message that will need to be broken into multiple blocks for RSA encryption."
    print(f"\nLonger Text Message: {longer_text}")
    
    # Encrypt in blocks
    encrypted_blocks = encrypt_large_text(longer_text, e, n)
    print(f"Number of encrypted blocks: {len(encrypted_blocks)}")
    first_few = encrypted_blocks[:3] if len(encrypted_blocks) > 3 else encrypted_blocks
    print(f"First few encrypted blocks: {first_few}")
    
    # Decrypt blocks
    decrypted_longer = decrypt_large_text(encrypted_blocks, d, n)
    print(f"Decrypted: {decrypted_longer}")
    
    print("\nRSA Implementation Complete!") 