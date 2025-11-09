import numpy as np
import base64
import random
try:
    from Crypto.Cipher import AES as _PyCryptoAES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
except ImportError:
    _PyCryptoAES = None

class CaesarCipher:
    @staticmethod
    def encrypt(text, key):
        if not key or not str(key).isdigit():
            raise ValueError("Caesar Cipher requires a numeric key.")
        shift = int(key) % 26
        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result

    @staticmethod
    def decrypt(text, key):
        if not key or not str(key).isdigit():
            raise ValueError("Caesar Cipher requires a numeric key.")
        return CaesarCipher.encrypt(text, -int(key))

class Rot13Cipher:
    @staticmethod
    def encrypt(text, key=None):
        if key:
            raise ValueError("ROT13 does not require a key.")
        return Rot13Cipher._rot13(text)

    @staticmethod
    def decrypt(text, key=None):
        if key:
            raise ValueError("ROT13 does not require a key.")
        return Rot13Cipher._rot13(text)

    @staticmethod
    def _rot13(text):
        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + 13) % 26 + base)
            else:
                result += char
        return result 

class PlayfairCipher:
    @staticmethod
    def _format_key(key):
        key = ''.join([c.upper() for c in key if c.isalpha()])
        seen = set()
        result = ''
        for c in key:
            if c == 'J': c = 'I'
            if c not in seen:
                seen.add(c)
                result += c
        for c in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if c not in seen:
                result += c
        return [result[i*5:(i+1)*5] for i in range(5)]

    @staticmethod
    def _find_position(matrix, char):
        for i, row in enumerate(matrix):
            if char in row:
                return i, row.index(char)
        return None

    @staticmethod
    def _process_text(text):
        text = ''.join([c.upper() for c in text if c.isalpha()])
        text = text.replace('J', 'I')
        i = 0
        result = ''
        while i < len(text):
            a = text[i]
            b = text[i+1] if i+1 < len(text) else 'X'
            if a == b:
                result += a + 'X'
                i += 1
            else:
                result += a + b
                i += 2
        if len(result) % 2 != 0:
            result += 'X'
        return result

    @staticmethod
    def encrypt(text, key):
        if not key:
            raise ValueError("Playfair Cipher requires a key.")
        matrix = PlayfairCipher._format_key(key)
        text = PlayfairCipher._process_text(text)
        result = ''
        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            r1, c1 = PlayfairCipher._find_position(matrix, a)
            r2, c2 = PlayfairCipher._find_position(matrix, b)
            if r1 == r2:
                result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
            elif c1 == c2:
                result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
            else:
                result += matrix[r1][c2] + matrix[r2][c1]
        return result

    @staticmethod
    def decrypt(text, key):
        if not key:
            raise ValueError("Playfair Cipher requires a key.")
        matrix = PlayfairCipher._format_key(key)
        text = ''.join([c.upper() for c in text if c.isalpha()])
        result = ''
        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            r1, c1 = PlayfairCipher._find_position(matrix, a)
            r2, c2 = PlayfairCipher._find_position(matrix, b)
            if r1 == r2:
                result += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
            elif c1 == c2:
                result += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
            else:
                result += matrix[r1][c2] + matrix[r2][c1]
        return result

class RailFenceCipher:
    @staticmethod
    def encrypt(text, key):
        if not key or not str(key).isdigit() or int(key) < 2:
            raise ValueError("Rail Fence Cipher requires a numeric key >= 2.")
        key = int(key)
        rails = ['' for _ in range(key)]
        rail = 0
        direction = 1
        for char in text:
            rails[rail] += char
            rail += direction
            if rail == 0 or rail == key-1:
                direction *= -1
        return ''.join(rails)

    @staticmethod
    def decrypt(text, key):
        if not key or not str(key).isdigit() or int(key) < 2:
            raise ValueError("Rail Fence Cipher requires a numeric key >= 2.")
        key = int(key)
        pattern = [0] * len(text)
        rail = 0
        direction = 1
        for i in range(len(text)):
            pattern[i] = rail
            rail += direction
            if rail == 0 or rail == key-1:
                direction *= -1
        rails = ['' for _ in range(key)]
        idx = 0
        for r in range(key):
            for i in range(len(text)):
                if pattern[i] == r:
                    rails[r] += text[idx]
                    idx += 1
        result = ''
        rail_indices = [0]*key
        for i in range(len(text)):
            r = pattern[i]
            result += rails[r][rail_indices[r]]
            rail_indices[r] += 1
        return result

class RowTranspositionCipher:
    @staticmethod
    def encrypt(text, key):
        if not key or not all(k.isdigit() for k in key.split()):
            raise ValueError("Row Transposition Cipher requires a numeric key (space-separated numbers, e.g. '3 1 2').")
        key_list = [int(k) for k in key.split()]
        n_cols = len(key_list)
        text = text.replace(' ', '')
        while len(text) % n_cols != 0:
            text += 'X'
        matrix = [text[i:i+n_cols] for i in range(0, len(text), n_cols)]
        result = ''
        for k in sorted((num, idx) for idx, num in enumerate(key_list)):
            col = k[1]
            for row in matrix:
                result += row[col]
        return result

    @staticmethod
    def decrypt(text, key):
        if not key or not all(k.isdigit() for k in key.split()):
            raise ValueError("Row Transposition Cipher requires a numeric key (space-separated numbers, e.g. '3 1 2').")
        key_list = [int(k) for k in key.split()]
        n_cols = len(key_list)
        n_rows = len(text) // n_cols
        matrix = [['']*n_cols for _ in range(n_rows)]
        idx = 0
        for k in sorted((num, idx) for idx, num in enumerate(key_list)):
            col = k[1]
            for row in range(n_rows):
                matrix[row][col] = text[idx]
                idx += 1
        result = ''.join(''.join(row) for row in matrix)
        return result.rstrip('X')

class HillCipher:
    @staticmethod
    def encrypt(text, key):
        if not key:
            raise ValueError("Hill Cipher requires a key (comma-separated numbers, e.g. '3,3,2,5').")
        key_nums = [int(x) for x in key.split(',') if x.strip().isdigit()]
        n = int(len(key_nums) ** 0.5)
        if n*n != len(key_nums):
            raise ValueError("Hill Cipher key must form a square matrix.")
        key_matrix = np.array(key_nums).reshape((n, n))
        text = ''.join([c.upper() for c in text if c.isalpha()])
        while len(text) % n != 0:
            text += 'X'
        result = ''
        for i in range(0, len(text), n):
            block = [ord(c) - ord('A') for c in text[i:i+n]]
            enc = np.dot(key_matrix, block) % 26
            result += ''.join(chr(e + ord('A')) for e in enc)
        return result

    @staticmethod
    def decrypt(text, key):
        if not key:
            raise ValueError("Hill Cipher requires a key (comma-separated numbers, e.g. '3,3,2,5').")
        key_nums = [int(x) for x in key.split(',') if x.strip().isdigit()]
        n = int(len(key_nums) ** 0.5)
        if n*n != len(key_nums):
            raise ValueError("Hill Cipher key must form a square matrix.")
        key_matrix = np.array(key_nums).reshape((n, n))
        det = int(round(np.linalg.det(key_matrix)))
        det_inv = pow(det, -1, 26)
        key_matrix_inv = (det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26)
        text = ''.join([c.upper() for c in text if c.isalpha()])
        result = ''
        for i in range(0, len(text), n):
            block = [ord(c) - ord('A') for c in text[i:i+n]]
            dec = np.dot(key_matrix_inv, block) % 26
            result += ''.join(chr(int(round(e)) + ord('A')) for e in dec)
        return result

class SubstitutionCipher:
    @staticmethod
    def encrypt(text, key):
        if not key or len(key) != 26 or not key.isalpha():
            raise ValueError("Substitution Cipher requires a 26-letter key.")
        key = key.upper()
        table = {chr(i+ord('A')): key[i] for i in range(26)}
        result = ''
        for c in text:
            if c.isalpha():
                up = c.isupper()
                sub = table[c.upper()]
                result += sub if up else sub.lower()
            else:
                result += c
        return result

    @staticmethod
    def decrypt(text, key):
        if not key or len(key) != 26 or not key.isalpha():
            raise ValueError("Substitution Cipher requires a 26-letter key.")
        key = key.upper()
        table = {key[i]: chr(i+ord('A')) for i in range(26)}
        result = ''
        for c in text:
            if c.isalpha():
                up = c.isupper()
                sub = table[c.upper()]
                result += sub if up else sub.lower()
            else:
                result += c
        return result

class VigenereCipher:
    @staticmethod
    def encrypt(text, key):
        if not key or not key.isalpha():
            raise ValueError("Vigenère Cipher requires an alphabetic key.")
        key = key.upper()
        result = ''
        j = 0
        for c in text:
            if c.isalpha():
                shift = ord(key[j % len(key)]) - ord('A')
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base + shift) % 26 + base)
                j += 1
            else:
                result += c
        return result

    @staticmethod
    def decrypt(text, key):
        if not key or not key.isalpha():
            raise ValueError("Vigenère Cipher requires an alphabetic key.")
        key = key.upper()
        result = ''
        j = 0
        for c in text:
            if c.isalpha():
                shift = ord(key[j % len(key)]) - ord('A')
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base - shift) % 26 + base)
                j += 1
            else:
                result += c
        return result

class ChrisWayV1Cipher:
    @staticmethod
    def encrypt(text, key=None):
        if not all(c.isalpha() or c.isspace() for c in text):
            raise ValueError("Input must contain only alphabetic characters and spaces.")
        
        text = ''.join(c for c in text if c.isalpha()).upper()
        if not text:
            return ""
        
        shifted = []
        for i, char in enumerate(text):
            base = ord('A')
            if i % 2 == 0:
                shift = i * 2
            else:
                shift = i + 3
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            shifted.append(shifted_char)
        
        # Swap characters: first with last, second with second-last, etc.
        n = len(shifted)
        swapped = [shifted[n - 1 - i] for i in range(n)]
        return ''.join(swapped)

    @staticmethod
    def decrypt(text, key=None):
        if not text or not all(c.isalpha() for c in text):
            raise ValueError("Encrypted text must contain only alphabetic characters.")
        
        text = text.upper()
        # Reverse the character swap
        n = len(text)
        reversed_swapped = [text[n - 1 - i] for i in range(n)]
        
        result = []
        for i, char in enumerate(reversed_swapped):
            base = ord('A')
            if i % 2 == 0:
                shift = i * 2
            else:
                shift = i + 3
            original_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(original_char)
        
        return ''.join(result)

    @staticmethod
    def encrypt(text, key=None):
        """
        Chris Way Cipher V1:
        - Even-indexed characters: Shift by char_index * 2
        - Odd-indexed characters: Shift by char_index + 3
        - Swap first with last, second with second-last, etc.
        
        Args:
            text (str): Plaintext to encrypt (alphabetic chars only)
            key: Not used in V1, included for interface compatibility
            
        Returns:
            str: Encrypted text
        """
        # Validate input - only alphabetic characters
        if not all(c.isalpha() or c.isspace() for c in text):
            raise ValueError("Input must contain only alphabetic characters and spaces.")
        
        # Remove spaces and convert to uppercase
        text = ''.join(c for c in text if c.isalpha()).upper()
        
        if not text:
            return ""
            
        # Step 1: Apply shifts based on position
        shifted = []
        for i, char in enumerate(text):
            if i % 2 == 0:  # Even index
                shift = i * 2
            else:  # Odd index
                shift = i + 3
            
            # Apply shift (ASCII of 'A' is 65)
            shifted_val = (ord(char) - ord('A') + shift) % 26
            shifted.append(chr(shifted_val + ord('A')))
        
        # Step 2: Swap characters
        result = list(shifted)
        for i in range(len(result) // 2):
            result[i], result[len(result) - 1 - i] = result[len(result) - 1 - i], result[i]
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text, key=None):
        """
        Decrypt text encrypted with Chris Way Cipher V1
        
        Args:
            text (str): Ciphertext to decrypt
            key: Not used in V1, included for interface compatibility
            
        Returns:
            str: Decrypted text
        """
        if not all(c.isalpha() for c in text):
            raise ValueError("Ciphertext must contain only alphabetic characters.")
            
        if not text:
            return ""
            
        # Step 1: Reverse the swaps
        result = list(text)
        for i in range(len(result) // 2):
            result[i], result[len(result) - 1 - i] = result[len(result) - 1 - i], result[i]
        
        # Step 2: Reverse the shifts
        decrypted = []
        for i, char in enumerate(result):
            if i % 2 == 0:  # Even index
                shift = i * 2
            else:  # Odd index
                shift = i + 3
            
            # Reverse the shift
            decrypted_val = (ord(char) - ord('A') - shift) % 26
            decrypted.append(chr(decrypted_val + ord('A')))
        
        return ''.join(decrypted)

class ChrisWayV2Cipher:
    @staticmethod
    def validate_key(key):
        """Validate that the key contains only alphabetic characters"""
        if not key:
            raise ValueError("Key cannot be empty.")
        if not all(c.isalpha() for c in key):
            raise ValueError("Key must contain only alphabetic characters.")
        if len(key) < 3:
            raise ValueError("Key should be at least 3 characters long for security.")
    
    @staticmethod
    def encrypt(text, key):
        """
        Chris Way Cipher V2 (Asymmetric):
        - Uses a public key to generate shifts based on ASCII values
        - Applies shifts and then character swapping
        
        Args:
            text (str): Plaintext to encrypt (alphabetic chars only)
            key (str): Public key for encryption
            
        Returns:
            str: Encrypted text
        """
        # Validate input
        if not all(c.isalpha() or c.isspace() for c in text):
            raise ValueError("Input must contain only alphabetic characters and spaces.")
        
        ChrisWayV2Cipher.validate_key(key)
        
        # Remove spaces and convert to uppercase
        text = ''.join(c for c in text if c.isalpha()).upper()
        key = key.upper()
        
        if not text:
            return ""
            
        # Step 1: Generate shifts from public key
        shifts = []
        for i in range(len(text)):
            key_char = key[i % len(key)]
            shift = (ord(key_char) - ord('A') + i) % 26
            shifts.append(shift)
        
        # Step 2: Apply shifts
        shifted = []
        for i, char in enumerate(text):
            shifted_val = (ord(char) - ord('A') + shifts[i]) % 26
            shifted.append(chr(shifted_val + ord('A')))
        
        # Step 3: Swap characters
        result = list(shifted)
        for i in range(len(result) // 2):
            result[i], result[len(result) - 1 - i] = result[len(result) - 1 - i], result[i]
        
        return ''.join(result)
    
    @staticmethod
    def decrypt(text, key):
        """
        Decrypt text encrypted with Chris Way Cipher V2
        
        Args:
            text (str): Ciphertext to decrypt
            key (str): Private key for decryption
            
        Returns:
            str: Decrypted text
        """
        # Validate input
        if not all(c.isalpha() for c in text):
            raise ValueError("Ciphertext must contain only alphabetic characters.")
        
        ChrisWayV2Cipher.validate_key(key)
        
        if not text:
            return ""
            
        key = key.upper()
        
        # Step 1: Reverse the swaps
        result = list(text)
        for i in range(len(result) // 2):
            result[i], result[len(result) - 1 - i] = result[len(result) - 1 - i], result[i]
        
        # Step 2: Generate shifts from private key
        shifts = []
        for i in range(len(text)):
            key_char = key[i % len(key)]
            shift = (ord(key_char) - ord('A') + i) % 26
            shifts.append(shift)
        
        # Step 3: Reverse the shifts
        decrypted = []
        for i, char in enumerate(result):
            decrypted_val = (ord(char) - ord('A') - shifts[i]) % 26
            decrypted.append(chr(decrypted_val + ord('A')))
        
        return ''.join(decrypted)

class AESCipher:
    @staticmethod
    def is_hex(s):
        """Check if a string is a valid hexadecimal value"""
        try:
            int(s, 16)
            return all(c in "0123456789ABCDEFabcdef" for c in s)
        except ValueError:
            return False

    @staticmethod
    def get_key_bytes(key):
        """Convert key to bytes, handling both text and hex formats
        
        Args:
            key: Either a regular text string or a hex string (detected by prefix '0x' or all hex chars)
            
        Returns:
            bytes: The key in bytes format
        """
        # Check if key is in hex format (either with 0x prefix or all hex chars)
        if key.startswith('0x') or AESCipher.is_hex(key):
            # Remove 0x prefix if present
            clean_key = key[2:] if key.startswith('0x') else key
            
            # Validate hex key length
            hex_lengths = [32, 48, 64]  # Valid hex string lengths for AES-128, AES-192, AES-256
            if len(clean_key) not in hex_lengths:
                raise ValueError(f"Hex key must be {', '.join(str(l) for l in hex_lengths)} characters long (got {len(clean_key)})")
                
            # Convert hex to bytes
            return bytes.fromhex(clean_key)
        else:
            # Regular text key
            if len(key) not in (16, 24, 32):
                raise ValueError("Text key must be 16, 24, or 32 characters long")
            return key.encode('utf-8')
    
    @staticmethod
    def encrypt(text, key, mode="CBC", output_format="base64"):
        """
        Encrypt data using AES
        
        Args:
            text: plaintext to encrypt
            key: encryption key (16, 24, or 32 bytes as text or 32, 48, or 64 hex chars)
            mode: encryption mode (CBC, GCM, CTR)
            output_format: 'base64' or 'hex'
        
        Returns:
            string: encoded IV/nonce and ciphertext in the specified format
        """
        if not _PyCryptoAES:
            raise ImportError("pycryptodome is required for AES.")
        
        # Convert key to bytes (handles both text and hex formats)
        key_bytes = AESCipher.get_key_bytes(key)
        data = text.encode('utf-8')
        
        # Use different modes with appropriate parameters
        if mode == "GCM":
            # GCM mode with authentication tag
            cipher = _PyCryptoAES.new(key_bytes, _PyCryptoAES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            
            # Encode components based on output format
            if output_format.lower() == "hex":
                nonce = cipher.nonce.hex()
                ct = ciphertext.hex()
                tag_str = tag.hex()
                return f"GCM:{nonce}:{ct}:{tag_str}"
            else:  # default to base64
                nonce = base64.b64encode(cipher.nonce).decode('utf-8')
                ct = base64.b64encode(ciphertext).decode('utf-8')
                tag_b64 = base64.b64encode(tag).decode('utf-8')
                return f"GCM:{nonce}:{ct}:{tag_b64}"
            
        elif mode == "CTR":
            # Counter mode
            cipher = _PyCryptoAES.new(key_bytes, _PyCryptoAES.MODE_CTR)
            ciphertext = cipher.encrypt(data)
            
            if output_format.lower() == "hex":
                nonce = cipher.nonce.hex()
                ct = ciphertext.hex()
                return f"CTR:{nonce}:{ct}"
            else:  # default to base64
                nonce = base64.b64encode(cipher.nonce).decode('utf-8')
                ct = base64.b64encode(ciphertext).decode('utf-8')
                return f"CTR:{nonce}:{ct}"
        
        else:  # Default CBC mode
            # CBC mode with padding (PKCS5Padding is equivalent to PKCS7Padding in PyCryptodome)
            cipher = _PyCryptoAES.new(key_bytes, _PyCryptoAES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data, _PyCryptoAES.block_size))
            
            if output_format.lower() == "hex":
                iv = cipher.iv.hex()
                ct = ct_bytes.hex()
                return f"CBC:{iv}:{ct}"
            else:  # default to base64
                iv = base64.b64encode(cipher.iv).decode('utf-8')
                ct = base64.b64encode(ct_bytes).decode('utf-8')
                return f"CBC:{iv}:{ct}"

    @staticmethod
    def decrypt(text, key):
        if not _PyCryptoAES:
            raise ImportError("pycryptodome is required for AES.")
        
        # Convert key to bytes (handles both text and hex formats)
        key_bytes = AESCipher.get_key_bytes(key)
        
        # Parse the ciphertext format to determine mode and parameters
        parts = text.split(':')
        mode = parts[0]
        
        if mode == "GCM":
            if len(parts) != 4:
                raise ValueError("Invalid GCM ciphertext format")
                
            # Try base64 first, fall back to hex if it fails
            try:
                nonce = base64.b64decode(parts[1])
                ciphertext = base64.b64decode(parts[2])
                tag = base64.b64decode(parts[3])
            except:
                # Try hex format
                nonce = bytes.fromhex(parts[1])
                ciphertext = bytes.fromhex(parts[2])
                tag = bytes.fromhex(parts[3])
            
            cipher = _PyCryptoAES.new(key_bytes, _PyCryptoAES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            
        elif mode == "CTR":
            if len(parts) != 3:
                raise ValueError("Invalid CTR ciphertext format")
                
            # Try base64 first, fall back to hex if it fails
            try:
                nonce = base64.b64decode(parts[1])
                ciphertext = base64.b64decode(parts[2])
            except:
                # Try hex format
                nonce = bytes.fromhex(parts[1])
                ciphertext = bytes.fromhex(parts[2])
            
            cipher = _PyCryptoAES.new(key_bytes, _PyCryptoAES.MODE_CTR, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            
        elif mode == "CBC":
            if len(parts) != 3:
                raise ValueError("Invalid CBC ciphertext format")
                
            # Try base64 first, fall back to hex if it fails
            try:
                iv = base64.b64decode(parts[1])
                ciphertext = base64.b64decode(parts[2])
            except:
                # Try hex format
                iv = bytes.fromhex(parts[1])
                ciphertext = bytes.fromhex(parts[2])
            
            cipher = _PyCryptoAES.new(key_bytes, _PyCryptoAES.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(ciphertext), _PyCryptoAES.block_size)
            
        else:
            # For backward compatibility with older format
            try:
                iv, ct = text.split(':')
                try:
                    iv = base64.b64decode(iv)
                    ct = base64.b64decode(ct)
                except:
                    # Try hex format
                    iv = bytes.fromhex(iv)
                    ct = bytes.fromhex(ct)
                    
                cipher = _PyCryptoAES.new(key_bytes, _PyCryptoAES.MODE_CBC, iv)
                plaintext = unpad(cipher.decrypt(ct), _PyCryptoAES.block_size)
            except Exception as e:
                raise ValueError(f"Unknown ciphertext format or decryption error: {str(e)}")
        
        return plaintext.decode('utf-8') 