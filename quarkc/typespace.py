from collections import OrderedDict
from .match import match, lazy, many, opt, choice

"""A type is represented as a node in a graph. There are two kinds of
nodes: Object and Callable. Edges are represented either implicitly
via containment (e.g. an Object may contain a Field that is a
Callable), or explicitly via a Ref.

Templates represent sets of similarly shaped nodes. A Ref to a
template must be supplied with parameters in order to select a single
node from within the set represented by the template.

Every node in the graph connects to other nodes via labeled
edges. Each labeled edge corresponds to a field name, argument
position, or return type depending on the particular kind of node the
edge is leaving.


An Object is composed of fields, and each field has a declared
type. An object is translated into a node by creating an edge labeled
by field name that connects to the node corresponding to the declared
type of each field:

    Declaration:

      object Foo {
          Bar field1;
          Baz field2;
      }

      object Bar {
          Foo field3;
      }

      object Baz {}

    Graph:

             field3
       +-----------------+
       |                 |
      \|/                |
      Foo---------->Bar--+
       |   field1
       |
       |
       | field2
       +-------->Baz


A Callable has a result type, and an expected type for each
argument. A Callable is translated into a graph by creating an edge
labeled by result and by argument position:

    Declaration:

      Baz fun(Foo, Bar)


    Graph:

           arg 1
       +--------->Foo
       |
       |   arg 2
      fun-------->Bar
       |
       |  result
       +--------->Baz


Object and Callable types can be mixed and matched:

    Declaration:

        object Mixed {
            Foo field;
            Baz fun(Foo, Bar);
        }


    Graph:

            field
         +------------------------------+
         |                              |
         |                      arg 1  \|/
       Mixed                +--------->Foo
         |                  |
         |  fun             |   arg 2
         +---------------->fun-------->Bar
                            |
                            |  result
                            +--------->Baz


A Template contains an Object or Callable with unbound references
(placeholder edges). When a Template node is referenced, these unbound
references are replaced with actual references:

    Declaration:

        object Box<T> {
            T contents;
        }

        object Foo {
            Box<Bar> field;
        }

        object Bar {}


    Implicit Declaration:

        object Box<Bar> {
            Bar contents;
        }


    Graph:

             field             contents
        Foo -------> Box<Bar> ----------> Bar


Object fields can be read/write or read only (final). A method is just
a read only field of a callable type.

Given this formalization, type equivalencies can be established by a
pairwise traversal of the graph from two starting points. The pairwise
traversal can be used to establish that any operation or sequence of
operations that can possibly be performed on one node has a
corresponding equivalence on the other node.

"""


class Base(object):
    """Base object that provides a convenient repr utility function."""

    def repr(self, *args):
        return "%s(%s)" % (self.__class__.__name__, ", ".join([repr(a) for a in args]))

class Ref(Base):

    """A reference to a node in the type graph."""

    @match(basestring, many(lazy("Ref")))
    def __init__(self, name, *params):
        self.name = name
        self.params = params

    def __hash__(self):
        return hash((self.name, self.params))

    def __eq__(self, other):
        return isinstance(other, Ref) and self.name == other.name and self.params == other.params

    def __ne__(self, other):
        return not (self == other)

    def bind(self, bindings):
        if self.name in bindings:
            assert not self.params
            return bindings.get(self.name)
        else:
            return Ref(self.name, *[p.bind(bindings) for p in self.params])

    def __repr__(self, *args):
        return self.repr(self.name, *self.params)

    def __str__(self):
        if self.params:
            return "{}<{}>".format(self.name, ", ".join([str(p) for p in self.params]))
        else:
            return self.name

class Type(Base):

    """Base class for Types. A type is represented as a node in a
    graph. Templates reperesent a set of similarly structured nodes.

    """

    pass

class Param(Type):

    """A parameter for a template."""

    @match(basestring, opt(Ref))
    def __init__(self, name, bound=None):
        self.name = name
        self.bound = bound

    def __repr__(self):
        if self.bound:
            return self.repr(self.name, self.bound)
        else:
            return self.repr(self.name)

class Unresolved(Type):
    pass

class UnresolvedRef(Unresolved):

    """Every unresolved reference points to this type.
    """

    @match(Ref)
    def __init__(self, ref):
        self.ref = ref

    def __repr__(self):
        return self.repr(self.ref)

class UnresolvedField(Unresolved):

    @match(Ref, basestring)
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self):
        return self.repr(self.type, self.name)

class UnresolvedCall(Unresolved):

    @match(Ref)
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return self.repr(self.type)

class Unresolvable(Unresolved):

    @match(choice(Unresolved, None))
    def __init__(self, un):
        self.un = un

class Typespace(object):

    """A typespace contains a set of nodes and provides the scope for
    resolving any references those nodes contains. It also contains
    methods for comparing types and for calculating the result type of
    operations such as invoking a callable or accessing a field.

    """

    def __init__(self):
        self.types = OrderedDict()
        self.resolved = OrderedDict()

    @match(basestring)
    def __getitem__(self, name):
        return self.types[name]

    @match(basestring, Type)
    def __setitem__(self, name, type):
        assert name not in self.types
        self.types[name] = type

    @match(basestring, lazy("Template"))
    def __setitem__(self, name, template):
        assert name not in self.types
        self.types[name] = template
        for p in template.params:
            if isinstance(p, Param):
                assert p.name not in self.types
                self.types[p.name] = p

    @match(Ref)
    def unresolve(self, ref):
        return ref

    @match(Type)
    def unresolve(self, type):
        for k, v in self.types.items():
            if v == type:
                return Ref(k)
        for k, v in self.resolved.items():
            if v == type:
                return k
        return type

    @match(Ref)
    def resolve(self, ref):
        """Resolve a reference."""

        if ref in self.resolved:
            return self.resolved[ref]
        if ref.name not in self.types:
            return UnresolvedRef(ref)
        type = self.types[ref.name]
        if ref.params:
            assert isinstance(type, Template)
            assert len(ref.params) == len(type.params)
            for r in ref.params:
                if isinstance(self.resolve(r), Unresolved):
                    return UnresolvedRef(ref)
            bindings = {}
            for p, v in zip(type.params, ref.params):
                bindings[p.name] = v
            type = type.bind(bindings)
        self.resolved[ref] = type
        return type

    @match(Type)
    def resolve(self, type):
        """This variant of resolve allows field, argument, and result types
        (or anywhere a reference may occur) to be specified as a
        nested anonymous types rather than being forced to have a
        name.

        """
        return type

    @match(Ref, basestring)
    def get(self, ref, name):
        """Calculate the result type of accessing a field.
        """
        return self.get(ref, self.resolve(ref), name)

    @match(Ref, lazy("Object"), basestring)
    def get(self, ref, object, name):
        """Calculate the result type of accessing a field.
        """
        field = object.byname.get(name, None)
        if field:
            return self.resolve(field.type)
        else:
            return UnresolvedField(ref, name)

    @match(Ref, lazy("Template"), basestring)
    def get(self, ref, template, name):
        return self.get(ref, template.type, name)

    @match(Ref, lazy("Param"), basestring)
    def get(self, ref, param, name):
        if param.bound:
            return self.get(ref, self.resolve(param.bound), name)
        else:
            return UnresolvedField(ref, name)

    @match(Unresolved, basestring)
    def get(self, un, name):
        return Unresolvable(un)

    @match(Ref, many(choice(Ref, Type)))
    def call(self, ref, *args):
        return self.call(self.resolve(ref), *args)

    @match(lazy("Callable"), many(choice(Ref, Type)))
    def call(self, callable, *args):
        """Calculate the result type of invoking a callable.
        """
        return self.resolve(callable.result)

    @match(Unresolved, many(choice(Ref, Type)))
    def call(self, un, *args):
        return Unresolvable(un)

    @match(Type, Type, opt(bool))
    def cotraverse(self, a, b, bidi=False, use_bounds=True):
        """This traversal yields a sequence of node pairs that must be
        compatible in order for node 'a' to have a subtype
        relationship with node 'b'.

        By traversing the type graph starting from node 'a', and
        making corresponding transitions starting from node 'b', we
        can establish that every operation that can be performed on a
        value of type 'a' can also be performed on a value of type
        'b'. This establishes liskov substitutability, aka a subtype
        relationship.

        If there is a transition on node 'a' or one of the nodes
        reachable from 'a' that does not have a corresponding
        transition on its companion node, the target of the transition
        is yielded by the generator with None as the companion
        node. (Should this be Unresolved?)

        """

        todo = [(a, b)]
        if bidi: todo.append((b, a))
        done = set()
        while todo:
            node, companion = todo.pop()
            key = (node, companion)
            if key in done:
                continue
            done.add(key)
            yield node, companion
            for n, c in self.cotransitions(node, companion, use_bounds):
                todo.append((n, c))

    @match(lazy("Object"), lazy("Object"), bool)
    def cotransitions(self, obj, companion, use_bounds):
        for f in obj.fields:
            cofield = companion.byname.get(f.name)
            if cofield:
                yield self.resolve(f.type), self.resolve(cofield.type)
                if f.writable:
                    if cofield.writable:
                        # invariant
                        yield self.resolve(cofield.type), self.resolve(f.type)
                    else:
                        yield self.resolve(f.type), None
            else:
                yield self.resolve(f.type), None

    @match(lazy("Object"), None, bool)
    def cotransitions(self, obj, companion, use_bounds):
        if False: yield

    @match(lazy("Callable"), lazy("Callable"), bool)
    def cotransitions(self, callable, companion, use_bounds):
        # covariant
        yield self.resolve(callable.result), self.resolve(companion.result)
        minargs = min(len(callable.arguments), len(companion.arguments))
        maxargs = max(len(callable.arguments), len(companion.arguments))
        idx = 0
        while idx < minargs:
            # contravariant
            yield self.resolve(companion.arguments[idx]), self.resolve(callable.arguments[idx])
            idx += 1
        while idx < maxargs:
            if idx < len(callable.arguments):
                yield self.resolve(callable.arguments[idx]), None
            else:
                yield self.resolve(companion.arguments[idx]), None
            idx += 1

    @match(lazy("Template"), lazy("Template"), bool)
    def cotransitions(self, template, companion, use_bounds):
        for a, b in self.cotransitions(template.type, companion.type, use_bounds):
            yield a, b

    @match(lazy("Object"), lazy("Param"), bool)
    def cotransitions(self, object, companion, use_bounds):
        if use_bounds:
            bound = self.resolve(companion.bound) if companion.bound else Object()
            for a, b in self.cotransitions(object, bound, use_bounds):
                yield a, b
        else:
            yield object, companion

    @match(lazy("Param"), lazy("Object"), bool)
    def cotransitions(self, param, companion, use_bounds):
        if use_bounds:
            bound = self.resolve(param.bound) if param.bound else Object()
            for a, b in self.cotransitions(bound, companion, use_bounds):
                yield a, b
        else:
            yield param, companion

    @match(lazy("Param"), lazy("Param"), bool)
    def cotransitions(self, param, companion, use_bounds):
        if use_bounds:
            left = self.resolve(param.bound) if param.bound else Object()
            right = self.resolve(companion.bound) if companion.bound else Object()
            for a, b in self.cotransitions(left, right, use_bounds):
                yield a, b
        else:
            yield param, companion

    @match(Ref, Ref)
    def assignable(self, a, b):
        return self.assignable(self.resolve(a), self.resolve(b))

    @match(Ref, Type)
    def assignable(self, a, b):
        return self.assignable(self.resolve(a), b)

    @match(Type, Ref)
    def assignable(self, a, b):
        return self.assignable(a, self.resolve(b))

    @match(Type, Type)
    def assignable(self, a, b):
        for n, m in self.cotraverse(a, b):
            if not self.compatible(n, m):
                return False
        return True

    @match(lazy("Template"), Type)
    def compatible(self, a, b):
        return False

    @match(lazy("Object"), Type)
    def compatible(self, a, b):
        return False

    @match(lazy("Callable"), Type)
    def compatible(self, a, b):
        return False

    @match(lazy("Object"), None)
    def compatible(self, a, b):
        return False

    @match(lazy("Callable"), None)
    def compatible(self, a, b):
        return False

    @match(lazy("Object"), lazy("Object"))
    def compatible(self, a, b):
        return True

    @match(lazy("Object"), lazy("Param"))
    def compatible(self, a, b):
        return True

    @match(lazy("Callable"), lazy("Callable"))
    def compatible(self, a, b):
        return len(a.arguments) == len(b.arguments)

    @match(lazy("Template"), lazy("Template"))
    def compatible(self, a, b):
        return len(a.params) == len(b.params)

    @match(lazy("Param"), lazy("Param"))
    def compatible(self, a, b):
        return True

    @match(lazy("Param"), None)
    def compatible(self, a, b):
        return False

    @match(lazy("Unresolved"), lazy("Unresolved"))
    def compatible(self, a, b):
        assert False, (a, b)

    @match(Type, Type)
    def infer(self, a, b):
        bindings = {}
        for n, m in self.cotraverse(a, b, use_bounds=False):
            self.add_inference(bindings, n, m)
        return bindings

    @match(dict, Type, Param)
    def add_inference(self, bindings, type, p):
        assert p.name not in bindings
        bindings[p.name] = self.unresolve(type)

    @match(dict, Param, Type)
    def add_inference(self, bindings, p, type):
        assert p.name not in bindings
        bindings[p.name] = self.unresolve(type)

    @match(dict, Type, Type)
    def add_inference(self, bindings, a, b):
        pass

class Field(Base):

    @match(basestring, choice(Ref, Type))
    def __init__(self, name, type):
        self.name = name
        self.type = type

    @property
    def writable(self):
        return True

    def bind(self, bindings):
        return self.__class__(self.name, self.type.bind(bindings))

    def __repr__(self):
        return self.repr(self.name, self.type)

class Final(Field):

    @property
    def writable(self):
        return False

class Object(Type):

    @match(many(Field))
    def __init__(self, *fields):
        self.fields = fields
        self.byname = {}
        for f in self.fields:
            assert f.name not in self.byname
            self.byname[f.name] = f

    @property
    def transitions(self):
        for f in self.fields:
            yield f.type

    def bind(self, bindings):
        return Object(*[f.bind(bindings) for f in self.fields])

    def __repr__(self):
        return self.repr(*self.fields)

class Callable(Type):

    @match(choice(Ref, Type), many(choice(Ref, Type)))
    def __init__(self, result, *arguments):
        self.result = result
        self.arguments = arguments

    def bind(self, bindings):
        return Callable(self.result.bind(bindings), *[f.bind(bindings) for f in self.arguments])

    def __repr__(self):
        return self.repr(self.result, *self.arguments)

class Template(Type):

    @match(many(choice(Param, Ref), min=1), choice(Object, Callable))
    def __init__(self, *args):
        self.params = args[:-1]
        self.type = args[-1]
        for p in self.params:
            if isinstance(p, Ref):
                assert not p.params

    @match(dict)
    def bind(self, bindings):
        return self.type.bind(bindings)

    def __repr__(self):
        return self.repr(*(self.params + (self.type,)))
