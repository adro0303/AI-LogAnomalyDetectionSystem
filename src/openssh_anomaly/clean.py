from typing import Dict, Optional

def clean_record(rec: Dict) -> Optional[Dict]:
    if not rec:
        return None
    if not rec.get('timestamp') or not rec.get('host') or not rec.get('message'):
        return None
    rec.setdefault('process', 'unknown')
    rec.setdefault('pid', -1)
    return rec
