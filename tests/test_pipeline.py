from src.openssh_anomaly.pipeline import parse_to_df, to_features, rolling_aggregates

def test_pipeline_end_to_end(tmp_path):
    # Crear archivo de log temporal
    log = tmp_path / 'auth.log'
    log.write_text('Jan 12 03:14:15 host1 sshd[1234]: Failed password for invalid user admin from 1.2.3.4 port 22 ssh2
')
    df = parse_to_df([str(log)], year=2020)
    feat = to_features(df)
    agg = rolling_aggregates(feat)
    assert len(agg) == 1
    assert 'fails_w' in agg.columns
