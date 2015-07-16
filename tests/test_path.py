from morf.path import Path


def test_resolve():
    obj = dict(
        a=dict(b=dict(c=1)),
        d=2,
    )
    assert Path.parse('/').resolve(obj) == obj
    assert Path.parse('/a').resolve(obj) == obj['a']
    assert Path.parse('/a/b').resolve(obj) == obj['a']['b']
    assert Path.parse('/a/b/c').resolve(obj) == obj['a']['b']['c']
    assert Path.parse('/d').resolve(obj) == obj['d']
