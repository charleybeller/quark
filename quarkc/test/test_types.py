import pytest
from quarkc.compiler import Compiler
from quarkc.match import match, choice, many
from quarkc.ast import (
    AST, Package, Declaration, Local, Param, Class, Function, PrimitiveLiteral, If, While, Block, Assign, ExprStmt,
    Return, Call, Attr, Var
)
from quarkc.parse import traversal
from quarkc.errors import InvalidInvocation, InvalidAssignment
from quarkc import typespace as types

class Base(object):

    def __ne__(self, other):
        return not (self == other)

class Constant(Base):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Constant) and self.name == other.name

    def __repr__(self):
        return self.name

DECLARE = Constant("DECLARE")
RETURN = Constant("RETURN")
IF = Constant("IF")
WHILE = Constant("WHILE")
CALLABLE = Constant("CALLABLE")
UNKNOWN = Constant("UNKNOWN")
ASSIGN = Constant("ASSIGN")
VIOLATION = Constant("VIOLATION")

def denest(t):
    if isinstance(t, tuple) and len(t) == 1:
        return t[0]
    else:
        return t

@match(choice(AST, [many(Package)]))
def exclude(n):
    return False

@match(Declaration)
def exclude(d):
    return exclude(d, d.parent)

@match(Declaration, Local)
def exclude(d, p):
    return True

@match(Param, AST)
def exclude(d, p):
    return True

@match(Declaration, AST)
def exclude(d, p):
    return False

def vcheck(c, node, result):
    for n in traversal(node):
        if n in c.types.violations and n not in c.reported:
            c.reported.add(n)
            return (VIOLATION, denest(tuple([vsig(v) for v in c.types.violations[n]])), result)
    return result

@match(InvalidInvocation)
def vsig(v):
    return v.expected, v.actual

@match(InvalidAssignment)
def vsig(v):
    return typesig(v.target), typesig(v.value)

@match(Compiler)
def typesigs(c):
    c.reported = set()
    result = {}
    for sym, node in c.symbols.definitions.items():
        if exclude(node): continue
        sig = typesig(c, node)
        if sig is not None:
            result[sym] = sig
    return result

@match(types.Callable)
def typesig(c):
    return (CALLABLE, typesig(c.result)) + tuple([typesig(a) for a in c.arguments])

@match(types.Object)
def typesig(o):
    return set(o.byname.keys())

@match(types.UnresolvedField)
def typesig(u):
    return (UNKNOWN, typesig(u.type), u.name)

@match(types.Ref)
def typesig(r):
    return str(r)

@match(Compiler, [many(Package)])
def typesig(c, pkgs):
    return None

@match(Compiler, choice(Class))
def typesig(c, cls):
    return None

@match(Compiler, Function)
def typesig(c, fun):
    sig = [typesig(c.types.node(fun))] + [typesig(c, p) for p in fun.params]
    if fun.body:
        sig.extend(typesig(c, fun.body))
    return vcheck(c, fun, denest(tuple(sig)))

@match(Compiler, PrimitiveLiteral)
def typesig(c, l):
    return vcheck(c, l, typesig(c.types[l]))

@match(Compiler, If)
def typesig(c, if_):
    result = (IF, typesig(c, if_.predicate), denest(typesig(c, if_.consequence)))
    if if_.alternative:
        result += (denest(typesig(c, if_.alternative)),)
    return vcheck(c, if_, result)

@match(Compiler, While)
def typesig(c, wh):
    return vcheck(c, wh, (WHILE, typesig(c, wh.condition), denest(typesig(c, wh.body))))

@match(Compiler, Block)
def typesig(c, block):
    return vcheck(c, block, tuple([typesig(c, s) for s in block.statements]))

@match(Compiler, Local)
def typesig(c, l):
    return vcheck(c, l, typesig(c, l.declaration))

@match(Compiler, choice(Declaration))
def typesig(c, nd):
    sig = str(c.types[nd])
    if nd.value:
        return vcheck(c, nd, (DECLARE, nd.name.text, sig, typesig(c, nd.value)))
    else:
        return vcheck(c, nd, (DECLARE, nd.name.text, sig))

@match(Compiler, Assign)
def typesig(c, ass):
    return vcheck(c, ass, (ASSIGN, typesig(c, ass.lhs), typesig(c, ass.rhs)))

@match(Compiler, Return)
def typesig(c, r):
    return vcheck(c, r, (RETURN, typesig(c, r.expr)))

@match(Compiler, choice(ExprStmt))
def typesig(c, stmt):
    return vcheck(c, stmt, typesig(c, stmt.expr))

@match(Compiler, choice(Call, Attr, Var))
def typesig(c, nd):
    return vcheck(c, nd, typesig(c.types[nd]))

def check(name, content, expected):
    c = Compiler()
    c.parse(name, content)
    c.check_symbols()
    c.check_types()
    assert expected == typesigs(c)

# XXX: if/while implies usage of bool!

def test_check():
    check("asdf", """
    namespace quark {
        interface void {}
        interface bool {}
        interface int {
            int __add__(int i);
            int __sub__(int i);
            bool __lt__(int i);
        }
    }
    void foo(void a) {
        int b;
        void c = foo(a);
        foo(b);
    }

    int fib(int n) {
        if (n < 2) {
            return n;
        } else {
            return fib(n-1) + fib(n-2);
        }
    }

    class Foo {
        int n = 0;
        int get() {
            return n;
        }
    }
    """,
    {'quark.int.__add__': ((CALLABLE, 'quark.int', 'quark.int'),
                           (DECLARE, 'i', 'quark.int')),
     'quark.int.__sub__': ((CALLABLE, 'quark.int', 'quark.int'),
                           (DECLARE, 'i', 'quark.int')),
     'quark.int.__lt__': ((CALLABLE, 'quark.bool', 'quark.int'),
                          (DECLARE, 'i', 'quark.int')),
     'asdf.foo': ((CALLABLE, 'quark.void', 'quark.void'),
                  (DECLARE, 'a', 'quark.void'),
                  (DECLARE, 'b', 'quark.int'),
                  (DECLARE, 'c', 'quark.void', 'quark.void'),
                  'quark.void'),
     'asdf.fib': ((CALLABLE, 'quark.int', 'quark.int'),
                  (DECLARE, 'n', 'quark.int'),
                  (IF, 'quark.bool',
                   (RETURN, 'quark.int'),
                   (RETURN, 'quark.int'))),
     'asdf.Foo.Foo': (CALLABLE, 'asdf.Foo'),
     'asdf.Foo.get': ((CALLABLE, 'quark.int'), (RETURN, 'quark.int')),
     'asdf.Foo.n': (DECLARE, 'n', 'quark.int', 'quark.int')})

def test_unknown_field():
    check("f",
          """
          class C {}

          C foo() {
              C.foo;
          }
          """,
          {
              'f.C.C': (CALLABLE, 'f.C'),
              'f.foo': ((CALLABLE, 'f.C'),
                        (UNKNOWN, 'f.C', 'foo'))
          })


@pytest.mark.xfail
def test_templated_field():
    check("f",
          """
          class X {}
          class C<T> {
              D<T> foo;
          }

          class D<T> { }

          C<X> foo() {
              C<X> f = new C<X>();
              D<X> g = f.foo;
          }
          """,
          {
              'f.X.X': (CALLABLE, 'f.X'),
              'f.C.C': (CALLABLE, 'f.C'),
              'f.D.D': (CALLABLE, 'f.D'),
              'f.foo': ((CALLABLE, 'f.C'),
                        (UNKNOWN, 'f.C', 'foo'))
          })


def check_violation(code, signature):
    prolog = """
        namespace quark {
            primitive void {}
            primitive bool {
                bool __eq__(bool b);
            }
            primitive int {
                int __add__(int n);
            }
            primitive String {
                String substring(int start, int len);
            }
        }
    """
    prolog_sig = {
        'quark.void.void': (CALLABLE, 'quark.void'),
        'quark.bool.bool': (CALLABLE, 'quark.bool'),
        'quark.bool.__eq__': ((CALLABLE, 'quark.bool', 'quark.bool'),
                              (DECLARE, 'b', 'quark.bool')),
        'quark.int.int': (CALLABLE, 'quark.int'),
        'quark.int.__add__': ((CALLABLE, 'quark.int', 'quark.int'),
                              (DECLARE, 'n', 'quark.int')),
        'quark.String.String': (CALLABLE, 'quark.String'),
        'quark.String.substring': ((CALLABLE, 'quark.String', 'quark.int', 'quark.int'),
                                   (DECLARE, 'start', 'quark.int'),
                                   (DECLARE, 'len', 'quark.int'))
    }
    signature.update(prolog_sig)
    check("f", prolog + code, signature)

def test_assignment_violation():
    check_violation(
        """
        int foo() {
            String x = 3;
            int y = "asdf";
            x = y;
            y = x;
        }
        """,
        {
            'f.foo': ((CALLABLE, 'quark.int'),
                      (VIOLATION, ('quark.String', 'quark.int'), (DECLARE, 'x', 'quark.String', 'quark.int')),
                      (VIOLATION, ('quark.int', 'quark.String'), (DECLARE, 'y', 'quark.int', 'quark.String')),
                      (VIOLATION, ('quark.String', 'quark.int'), (ASSIGN, 'quark.String', 'quark.int')),
                      (VIOLATION, ('quark.int', 'quark.String'), (ASSIGN, 'quark.int', 'quark.String'))),
        })

def test_return_violation():
    check_violation(
        """
        int foo() {
            return "three";
        }
        """,
        {
            'f.foo': ((CALLABLE, 'quark.int'),
                      (VIOLATION, ('quark.int', 'quark.String'), (RETURN, 'quark.String')))
        })

def test_call_violation():
    check_violation(
        """
        void foo(String s) {
          foo(3);
          foo("three", 4);
        }
        """,
        {
            'f.foo': ((CALLABLE, 'quark.void', 'quark.String'),
                      (DECLARE, 's', 'quark.String'),
                      (VIOLATION, ('quark.String', 'quark.int'), 'quark.void'),
                      (VIOLATION, (1, 2), 'quark.void'))
        }
    )

def test_bool_violation():
    check_violation(
        """
        void foo() {
           if (foo()) {}
           while (foo()) {}
        }
        """,
        {
            'f.foo': ((CALLABLE, 'quark.void'),
                      (VIOLATION, ('quark.bool', 'quark.void'), (IF, 'quark.void', ())),
                      (VIOLATION, ('quark.bool', 'quark.void'), (WHILE, 'quark.void', ())))
        }
    )