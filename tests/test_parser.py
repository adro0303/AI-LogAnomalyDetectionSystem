from src.openssh_anomaly.parser import parse_line

def test_parse_line_basic():
    line = 'Jan 12 03:14:15 host1 sshd[1234]: Failed password for invalid user admin from 1.2.3.4 port 22 ssh2'
    rec = parse_line(line, year=2020)
    assert rec is not None
    assert rec['host'] == 'host1'
    assert 'Failed password' in rec['message']
