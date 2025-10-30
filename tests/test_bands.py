from eegviz.analysis.bands import bandpower_mean

def test_bandpower(make_raw_sine):
    raw = make_raw_sine(freq=10.0)
    bp = bandpower_mean(raw, 8.0, 13.0)
    assert (bp > 0).all()
