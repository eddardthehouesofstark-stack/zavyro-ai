from datetime import datetime, timezone
import random


def generate_ticket_number(sequence_id: int) -> str:
    year = datetime.now(timezone.utc).year
    return f"HD-{year}-{sequence_id:06d}"
