import re
from datetime import datetime, timezone
from typing import Optional, Dict

LINE_RE = re.compile(
    r'^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<process>\S+)(?:\[(?P<pid>\d+)\])?:\s+(?P<message>.*)$'
)
MONTHS = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

def parse_line(line: str, year: int = 2020) -> Optional[Dict]:
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    md = m.groupdict()
    try:
        ts = datetime(
            year=year,
            month=MONTHS.get(md['month'], 1),
            day=int(md['day']),
            hour=int(md['time'][0:2]),
            minute=int(md['time'][3:5]),
            second=int(md['time'][6:8]),
            tzinfo=timezone.utc,
        )
    except Exception:
        return None

    return {
        'timestamp': ts.isoformat(),
        'host': md['host'],
        'process': md['process'],
        'pid': int(md['pid']) if md.get('pid') else -1,
        'message': md['message'],
    }
