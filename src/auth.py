import sqlite3
import os
import hashlib
import secrets
from datetime import datetime, timedelta


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = "data"
AUTH_DATABASE_PATH = os.path.join(DATA_DIR, "auth.db")


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_auth_connection():
    os.makedirs(DATA_DIR, exist_ok=True)
    return sqlite3.connect(AUTH_DATABASE_PATH)


# ============================================================
# INITIALIZE AUTH DATABASE
# ============================================================

def init_auth_db():
    connection = get_auth_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            reset_code TEXT,
            reset_code_expires TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # --------------------------------------------------------
    # Migration for an existing auth.db
    # --------------------------------------------------------

    try:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN reset_code TEXT"
        )
    except sqlite3.OperationalError:
        # Column already exists
        pass

    try:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN reset_code_expires TEXT"
        )
    except sqlite3.OperationalError:
        # Column already exists
        pass

    connection.commit()
    connection.close()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Hash a password using PBKDF2-HMAC-SHA256
    with a random salt.
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000,
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(password, stored_password):
    """
    Verify a password against the stored
    salt:hash format.
    """

    try:
        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(hash_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000,
        )

        return secrets.compare_digest(
            password_hash,
            stored_hash,
        )

    except (ValueError, TypeError):
        return False


# ============================================================
# EMAIL VALIDATION
# ============================================================

def validate_email(email):
    email = email.strip().lower()

    if not email:
        return False

    if "@" not in email:
        return False

    if "." not in email.split("@")[-1]:
        return False

    return True


# ============================================================
# REGISTER USER
# ============================================================

def register_user(name, email, password):

    init_auth_db()

    name = name.strip()
    email = email.strip().lower()

    # Validate name
    if not name:
        return (
            False,
            "Name is required.",
            None,
        )

    # Validate email
    if not validate_email(email):
        return (
            False,
            "Please enter a valid email address.",
            None,
        )

    # Validate password
    if len(password) < 8:
        return (
            False,
            "Password must contain at least 8 characters.",
            None,
        )

    password_hash = hash_password(password)

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password_hash,
            ),
        )

        connection.commit()

        user_id = cursor.lastrowid

        return (
            True,
            "Account created successfully.",
            user_id,
        )

    except sqlite3.IntegrityError:

        return (
            False,
            "An account with this email already exists.",
            None,
        )

    except Exception as exc:

        return (
            False,
            f"Registration failed: {exc}",
            None,
        )

    finally:
        connection.close()


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(email, password):

    init_auth_db()

    email = email.strip().lower()

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        user = cursor.fetchone()

        if user is None:

            return {
                "success": False,
                "message": "Invalid email or password.",
            }

        user_id = user[0]
        name = user[1]
        stored_email = user[2]
        stored_password = user[3]

        if not verify_password(
            password,
            stored_password,
        ):

            return {
                "success": False,
                "message": "Invalid email or password.",
            }

        return {
            "success": True,
            "user_id": user_id,
            "name": name,
            "email": stored_email,
        }

    finally:
        connection.close()


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(user_id):

    init_auth_db()

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                created_at
            FROM users
            WHERE id = ?
            """,
            (int(user_id),),
        )

        user = cursor.fetchone()

        if user is None:
            return None

        return {
            "user_id": user[0],
            "name": user[1],
            "email": user[2],
            "created_at": user[3],
        }

    finally:
        connection.close()


# ============================================================
# CHECK IF EMAIL EXISTS
# ============================================================

def email_exists(email):

    init_auth_db()

    email = email.strip().lower()

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE email = ?
            LIMIT 1
            """,
            (email,),
        )

        return cursor.fetchone() is not None

    finally:
        connection.close()


# ============================================================
# CREATE PASSWORD RESET CODE
# ============================================================

def create_password_reset_code(email):

    init_auth_db()

    email = email.strip().lower()

    # Validate email
    if not validate_email(email):

        return (
            False,
            "Please enter a valid email address.",
            None,
        )

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        # Check whether account exists
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        user = cursor.fetchone()

        if user is None:

            return (
                False,
                "No account found with this email address.",
                None,
            )

        # Generate a 6-digit reset code
        reset_code = str(
            secrets.randbelow(900000) + 100000
        )

        # Code valid for 10 minutes
        expires_at = (
            datetime.now()
            + timedelta(minutes=10)
        ).isoformat()

        cursor.execute(
            """
            UPDATE users
            SET
                reset_code = ?,
                reset_code_expires = ?
            WHERE email = ?
            """,
            (
                reset_code,
                expires_at,
                email,
            ),
        )

        connection.commit()

        return (
            True,
            "Reset code generated successfully.",
            reset_code,
        )

    except Exception as exc:

        return (
            False,
            f"Unable to generate reset code: {exc}",
            None,
        )

    finally:
        connection.close()


# ============================================================
# RESET PASSWORD
# ============================================================

def reset_password(
    email,
    reset_code,
    new_password,
):

    init_auth_db()

    email = email.strip().lower()
    reset_code = reset_code.strip()

    # Validate new password
    if len(new_password) < 8:

        return (
            False,
            "Password must contain at least 8 characters.",
        )

    connection = get_auth_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                reset_code,
                reset_code_expires
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        user = cursor.fetchone()

        if user is None:

            return (
                False,
                "Account not found.",
            )

        stored_code = user[0]
        expires_at = user[1]

        # Check code exists
        if not stored_code:

            return (
                False,
                "No active reset code found.",
            )

        # Check code matches
        if stored_code != reset_code:

            return (
                False,
                "Invalid reset code.",
            )

        # Check expiration exists
        if not expires_at:

            return (
                False,
                "Reset code has expired.",
            )

        # Check expiration
        try:

            expiration_time = datetime.fromisoformat(
                expires_at
            )

        except ValueError:

            return (
                False,
                "Invalid reset code expiration.",
            )

        if datetime.now() > expiration_time:

            return (
                False,
                "Reset code has expired.",
            )

        # Create new password hash
        new_password_hash = hash_password(
            new_password
        )

        # Update password and remove reset code
        cursor.execute(
            """
            UPDATE users
            SET
                password_hash = ?,
                reset_code = NULL,
                reset_code_expires = NULL
            WHERE email = ?
            """,
            (
                new_password_hash,
                email,
            ),
        )

        connection.commit()

        return (
            True,
            "Password reset successfully.",
        )

    except Exception as exc:

        connection.rollback()

        return (
            False,
            f"Password reset failed: {exc}",
        )

    finally:
        connection.close()