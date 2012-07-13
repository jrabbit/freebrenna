#py.test

import main

def simple(t):
    return main.FreeBreanna(f=str(t.join('test.db')))

def test_uplimit(tmpdir):
    fb = simple(tmpdir)
    fb.s['count'] = 9001
    assert fb.islimited() == True

def test_underlimit(tmpdir):
    fb = simple(tmpdir)
    fb.s['count'] = 400
    assert fb.islimited() == False

