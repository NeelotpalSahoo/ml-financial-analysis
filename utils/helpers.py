def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def format_percent(value):
    try:
        return f"{float(value):.2f}%"
    except:
        return "N/A"

def truncate_text(text, limit=200):
    return (text[:limit] + '...') if len(text) > limit else text
