#!/usr/bin/env python3
"""
Auth module to handle password hashing and authentication.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with a salt.

    Args:
        password (str): The password string to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Encode the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password
