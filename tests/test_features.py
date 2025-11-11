from src.openssh_anomaly.features import feature_row

def test_feature_row_flags():
    rec = {'timestamp':'2020-01-01T00:00:00Z','host':'h','process':'sshd','pid':1,'message':'Failed password for user from 1.2.3.4 port 22 ssh2'}
    f = feature_row(rec)
    assert f['is_failed'] == 1
    assert f['msg_len'] > 0
