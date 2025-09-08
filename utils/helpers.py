def hours_to_minutes(hours: int, minutes: int) -> int:
    return hours * 60 + minutes

def minutes_to_hours(minutes: int) -> str:
    h = minutes // 60
    m = minutes % 60
    return f"{h}:{m:02d}"