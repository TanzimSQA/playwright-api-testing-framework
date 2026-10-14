import time
import random
import string
from typing import Dict, Any


def random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_fake_product() -> Dict[str, Any]:
    """Generate dynamic payload for creating a new product."""
    unique_suffix = f"{int(time.time())}_{random_string(4)}"
    return {
        "title": f"Automated Test Product {unique_suffix}",
        "price": round(random.uniform(10.0, 999.0), 2),
        "description": f"High quality automated test item created during test run {unique_suffix}",
        "category": random.choice(["smartphones", "laptops", "fragrances", "groceries", "beauty"]),
        "stock": random.randint(1, 100),
    }


def generate_fake_credentials() -> Dict[str, str]:
    """Generate randomized non-existent user credentials for negative testing."""
    return {
        "username": f"nonexistent_{random_string(6)}",
        "password": f"invalid_pwd_{random_string(8)}",
    }
