from quark_runtime import *


def test1():
    map = _Map();
    (map)[u"pi"] = (3);
    _println((map).get(u"pi"));
    _println((map).get(u"not_there"));
    _println(u"^--- should be null");


def test_update():
    first = _Map();
    second = _Map();
    (first)[u"a"] = (u"first_a");
    (first)[u"b"] = (u"first_b");
    (second)[u"b"] = (u"second_b");
    (second)[u"c"] = (u"second_c");
    (first).update(second);
    _println((first).get(u"a"));
    _println((first).get(u"b"));
    _println((first).get(u"c"));


def main():
    test1();
    test_update();


if __name__ == "__main__":
    main()
