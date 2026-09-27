import sqlite3
import csv
import os


# ============================================================
# PATHS
# ============================================================

DATA_DIR = "data"
USERS_DIR = os.path.join(DATA_DIR, "users")

LEGACY_DATABASE_PATH = os.path.join(DATA_DIR, "finance.db")

TRANSACTIONS_CSV = os.path.join(DATA_DIR, "transactions.csv")
BUDGETS_CSV = os.path.join(DATA_DIR, "budgets.csv")


# ============================================================
# CURRENT USER CONTEXT
# ============================================================

_CURRENT_USER_ID = None


def set_current_user(user_id):
    """
    Set the authenticated user for the current application session.
    """
    global _CURRENT_USER_ID

    if user_id is None:
        raise ValueError("user_id cannot be None.")

    _CURRENT_USER_ID = int(user_id)


def clear_current_user():
    """
    Clear the currently authenticated user.
    """
    global _CURRENT_USER_ID
    _CURRENT_USER_ID = None


def get_current_user_id():
    """
    Return the currently authenticated user ID.
    """
    return _CURRENT_USER_ID


# ============================================================
# DIRECTORIES
# ============================================================

def ensure_data_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(USERS_DIR, exist_ok=True)


# ============================================================
# USER DATABASE
# ============================================================

def get_user_db_path(user_id):
    if user_id is None:
        raise ValueError("user_id is required for a user database.")

    ensure_data_directories()

    return os.path.join(
        USERS_DIR,
        f"user_{int(user_id)}.db"
    )


def get_user_connection(user_id):
    """
    Return a SQLite connection for a specific user.
    """
    db_path = get_user_db_path(user_id)

    connection = sqlite3.connect(db_path)

    return connection


# ============================================================
# MAIN APPLICATION CONNECTION
# ============================================================

def get_connection():
    """
    Return the database connection for the authenticated user.

    All application modules should use this function.
    """

    if _CURRENT_USER_ID is None:
        raise RuntimeError(
            "No authenticated user is set. "
            "Call set_current_user(user_id) after login."
        )

    return get_user_connection(_CURRENT_USER_ID)


# ============================================================
# USER DATABASE TABLES
# ============================================================

def create_tables(user_id):
    connection = get_user_connection(user_id)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            payment_method TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            budget REAL NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS app_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# DEMO DATA
# ============================================================

def load_demo_data(user_id):
    connection = get_user_connection(user_id)

    cursor = connection.cursor()

    # --------------------------------------------------------
    # TRANSACTIONS
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    transaction_count = cursor.fetchone()[0]

    if (
        transaction_count == 0
        and os.path.exists(TRANSACTIONS_CSV)
    ):
        with open(
            TRANSACTIONS_CSV,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            records = []

            for row in reader:

                records.append(
                    (
                        row["date"],
                        row["type"],
                        row["category"],
                        row["description"],
                        float(row["amount"]),
                        row["payment_method"],
                    )
                )

        if records:

            cursor.executemany(
                """
                INSERT INTO transactions
                (
                    date,
                    type,
                    category,
                    description,
                    amount,
                    payment_method
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                records
            )

    # --------------------------------------------------------
    # BUDGETS
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM budgets"
    )

    budget_count = cursor.fetchone()[0]

    if (
        budget_count == 0
        and os.path.exists(BUDGETS_CSV)
    ):
        with open(
            BUDGETS_CSV,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            records = []

            for row in reader:

                records.append(
                    (
                        row["category"],
                        float(row["budget"])
                    )
                )

        if records:

            cursor.executemany(
                """
                INSERT OR IGNORE INTO budgets
                (
                    category,
                    budget
                )
                VALUES (?, ?)
                """,
                records
            )

    connection.commit()
    connection.close()


# ============================================================
# INITIALIZE USER DATABASE
# ============================================================

def initialize_user_database(
    user_id,
    load_demo=True
):
    """
    Create and optionally populate a user's database.
    """

    if user_id is None:
        raise ValueError(
            "Cannot initialize database without user_id."
        )

    create_tables(user_id)

    if load_demo:
        load_demo_data(user_id)


# ============================================================
# USER DATABASE CHECK
# ============================================================

def user_database_exists(user_id):

    if user_id is None:
        return False

    return os.path.exists(
        get_user_db_path(user_id)
    )


# ============================================================
# DELETE USER DATABASE
# ============================================================

def delete_user_database(user_id):

    db_path = get_user_db_path(user_id)

    if os.path.exists(db_path):
        os.remove(db_path)


# ============================================================
# LEGACY DATABASE
# ============================================================

def create_legacy_tables():

    ensure_data_directories()

    connection = sqlite3.connect(
        LEGACY_DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            payment_method TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            budget REAL NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def get_legacy_data_counts():

    create_legacy_tables()

    connection = sqlite3.connect(
        LEGACY_DATABASE_PATH
    )

    cursor = connection.cursor()

    transaction_count = cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    budget_count = cursor.execute(
        "SELECT COUNT(*) FROM budgets"
    ).fetchone()[0]

    connection.close()

    return {
        "transactions": transaction_count,
        "budgets": budget_count,
    }


def initialize_database():
    """
    Compatibility function for the old finance.db.

    The authenticated application should use
    initialize_user_database(user_id) instead.
    """

    create_legacy_tables()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    initialize_database()

    print(
        "✅ Legacy database ready!"
    )