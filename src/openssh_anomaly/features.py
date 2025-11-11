import re
from typing import Dict

def message_template(msg: str) -> str:
    msg = re.sub(r'\d{1,3}(?:\.\d{1,3}){3}', '<IP>', msg)
    msg = re.sub(r'[0-9A-Fa-f:]{2,}', '<HEX>', msg)
    msg = re.sub(r'\d+', '<NUM>', msg)
    return msg

def feature_row(rec: Dict) -> Dict:
    msg = rec['message']
    templ = message_template(msg)
    return {
        'timestamp': rec['timestamp'],
        'host': rec['host'],
        'process': rec['process'],
        'pid': rec['pid'],
        'msg_len': len(msg),
        'templ': templ,
        'is_failed': int('Failed password' in msg),
        'is_accepted': int('Accepted password' in msg or 'Accepted publickey' in msg),
    }
