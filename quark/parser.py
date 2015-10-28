# Copyright 2015 datawire. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .ast import *
from grammar import ParseError
import grammar

g = grammar.Grammar()

@g.parser
class Parser:

    keywords = ["package", "class", "interface", "primitive", "extends",
                "return", "macro", "new", "null", "if", "else", "while",
                "super", "true", "false"]
    symbols = {"LBR": "{",
               "RBR": "}",
               "LBK": "[",
               "RBK": "]",
               "LPR": "(",
               "RPR": ")",
               "LA": "<",
               "RA": ">",
               "COLON": ":",
               "COMMA": ",",
               "SEMI": ";",
               "EQ": "=",
               "PLUS": "+",
               "MINUS": "-",
               "NOT": "!",
               "TWIDDLE": "~",
               "DOT": ".",
               "MUL": "*",
               "DIV": "/",
               "MOD": "%",
               "GE": ">=",
               "LE": "<=",
               "LT": "<",
               "GT": ">",
               "EQL": "==",
               "NEQ": "!=",
               "AND": "&&",
               "OR": "||",
               "AT": "@"}

    aliases = {
        "+": "__add__",
        "-": "__sub__",
        "*": "__mul__",
        "/": "__div__",
        "%": "__mod__",
        "&&": "__and__",
        "||": "__or__",
        "<=": "__le__",
        ">=": "__ge__",
        "<": "__lt__",
        ">": "__gt__",
        "==": "__eq__",
        "!=": "__ne__"
    }

    unary_aliases = {
        "!": "__not__",
        "-": "__neg__"
    }

    @g.rule('file = file_definition* ~"$"')
    def visit_file(self, node, (definitions, eof)):
        return File(definitions)

    @g.rule('file_definition = annotation* (package / class / function / macro)')
    def visit_file_definition(self, node, (annotations, (dfn,))):
        dfn.annotations = annotations
        return dfn

    @g.rule('annotation = ann_name (LPR exprs RPR)?')
    def visit_annotation(self, node, (name, opt)):
        if opt:
            exprs = opt[0][1]
        else:
            exprs = []
        return Annotation(name, exprs)

    @g.rule('ann_name = AT name_re _')
    def visit_ann_name(self, node, (a, name, _)):
        return Name(name)

    @g.rule('package = PACKAGE name LBR pkg_definition* RBR')
    def visit_package(self, node, children):
        _, name, _, definitions, _ = children
        return Package(name, definitions)

    @g.rule('pkg_definition = annotation* (package / class / function)')
    def visit_pkg_definition(self, node, (annotations, (dfn,))):
        dfn.annotations = annotations
        return dfn

    @g.rule('class = (CLASS / INTERFACE / PRIMITIVE) name type_params? ( EXTENDS type )? LBR class_definition* RBR')
    def visit_class(self, node, ((kw,), name, params, extends, l, definitions, r)):
        if params:
            params = params[0]
        else:
            params = []
        if extends:
            base = extends[0][-1]
        else:
            base = None

        if kw == "class":
            return Class(name, params, base, definitions)
        elif kw == "interface":
            return Interface(name, params, base, definitions)
        else:
            return Primitive(name, params, base, definitions)

    @g.rule('type_params = LA type_param (COMMA type_param)* RA')
    def visit_type_params(self, node, (l, first, rest, r)):
        return [first] + [n[-1] for n in rest]

    @g.rule('type_param = name ""')
    def visit_type_param(self, node, (name, _)):
        return TypeParam(name)

    @g.rule('class_definition = annotation* (field / constructor / method / constructor_macro / method_macro)')
    def visit_class_definition(self, node, (annotations, (dfn,))):
        dfn.annotations = annotations
        return dfn

    @g.rule('field = type name (EQ expr)? SEMI')
    def visit_field(self, node, (type, name, opt, _)):
        if opt:
            expr = opt[0][-1]
        else:
            expr = None
        return Field(type, name, expr)

    @g.rule('constructor = name LPR parameters RPR block')
    def visit_constructor(self, node, (name, lp, parameters, rp, body)):
        return Constructor(name, tuple(parameters), body)

    @g.rule('constructor_macro = MACRO name LPR parameters RPR expr SEMI')
    def visit_constructor_macro(self, node, (m, name, lp, parameters, rp, expr, s)):
        return ConstructorMacro(name, tuple(parameters), expr)

    @g.rule('method = type name LPR parameters RPR body')
    def visit_method(self, node, (type, name, lp, parameters, rp, body)):
        return Method(type, name, tuple(parameters), body)

    @g.rule('body = block / SEMI')
    def visit_body(self, node, (child,)):
        if isinstance(child, Block):
            return child
        else:
            return None

    @g.rule('method_macro = MACRO type name LPR parameters RPR expr SEMI')
    def visit_method_macro(self, node, (macro, type, name, lp, parameters, rp, expr, s)):
        return MethodMacro(type, name, tuple(parameters), expr)

    @g.rule('function = type name LPR parameters RPR block')
    def visit_function(self, node, (type, name, lp, parameters, rp, body)):
        return Function(type, name, tuple(parameters), body)

    @g.rule('macro = MACRO type name LPR parameters RPR expr SEMI')
    def visit_macro(self, node, (macro, type, name, lp, parameters, rp, expr, s)):
        return Macro(type, name, tuple(parameters), expr)

    @g.rule('parameters = (param (COMMA param)*)?')
    def visit_parameters(self, node, children):
        if children:
            children = children[0]
            if children[1]:
                children[1:] = map(lambda x: x[-1], children[1])
            else:
                del children[1]
        return children

    @g.rule('param = type name (EQ expr)?')
    def visit_param(self, node, (type, name, opt)):
        if opt:
            expr = opt[0][-1]
        else:
            expr = None
        return Param(type, name, expr)

    @g.rule('type = dotted_name (LA types RA)?')
    def visit_type(self, node, (path, params)):
        if params:
            _, types, _ = params[0]
            return Type(path, types)
        else:
            return Type(path)

    @g.rule('dotted_name = name (DOT name)*')
    def visit_dotted_name(self, node, (first, rest)):
        return [first] + [n[-1] for n in rest]

    @g.rule('types = type (COMMA type)*')
    def visit_types(self, node, (first, rest)):
        return [first] + [n[-1] for n in rest]

    @g.rule('name_re = ~"[_a-zA-Z][_a-zA-Z0-9]*"')
    def visit_name_re(self, node, children):
        return node.text

    @g.rule('name = _ name_re  _')
    def visit_name(self, node, (pre, name, post)):
        return Name(name)

    # XXX: local declarations and exprstmt are ambiguous, e.g.:
    #   Box<int> x; looks like a declaration
    #      vs
    #    a < b > c; looks like a comparison
    @g.rule('statement = return / assign / local / if / while / exprstmt')
    def visit_statement(self, node, (stmt,)):
        return stmt

    @g.rule('return = RETURN expr? SEMI')
    def visit_return(self, node, (r, opt, s)):
        expr = opt[0] if opt else None
        return Return(expr)

    @g.rule('exprstmt = expr SEMI')
    def visit_exprstmt(self, node, (expr, s)):
        return ExprStmt(expr)

    @g.rule('assign = ( lval / lvar )  EQ expr SEMI')
    def visit_assign(self, node, ((lhs,), eq, rhs, s)):
        return lhs(rhs)

    @g.rule('lval = atom (callmod? (attrmod / getmod))+')
    def visit_lval(self, node, (atom, mods)):
        result = atom
        for (opt, mod) in mods[:-1]:
            if opt: result = opt[0](result)
            result = mod[0](result)
        opt, lastmod = mods[-1]
        if opt: result = opt[0](result)
        mod = lastmod[0]
        return lambda rhs: mod.assign(result, rhs)

    @g.rule('lvar = var ""')
    def visit_lvar(self, node, (var, _)):
        return lambda rhs: Assign(var, rhs)

    @g.rule('set = atom ((callmod / attrmod)? getmod)+')
    def visit_set(self, node, (atom, mods)):
        result = atom
        for (opt, get) in mods[:1]:
            if opt:
                result = opt[0][0](result)
            result = get(result)
        get = mods[-1][-1]
        return lambda rhs: get(result, '__set__', [rhs])

    @g.rule('local = type name (EQ expr)? SEMI')
    def visit_local(self, node, (type, name, opt, _)):
        if opt:
            expr = opt[0][-1]
        else:
            expr = None
        return Local(Declaration(type, name, expr))

    @g.rule('if = IF LPR expr RPR block (ELSE block)?')
    def visit_if(self, node, (kw, lp, expr, rp, consequence, opt)):
        if opt:
            alternative = opt[0][1]
        else:
            alternative = None
        return If(expr, consequence, alternative)

    @g.rule('block = LBR statements RBR')
    def visit_block(self, node, (l, statements, r)):
        return Block(statements)

    @g.rule('statements = statement*')
    def visit_statements(self, node, children):
        return children

    @g.rule('while = WHILE LPR expr RPR block')
    def visit_while(self, node, (kw, lp, expr, rp, body)):
        return While(expr, body)

    @g.rule('expr = oroperand (OR oroperand)*')
    def visit_expr(self, node, (result, remaining)):
        while remaining:
            op, rhs = remaining.pop(0)
            result = Call(Attr(result, Name(self.aliases[op])), [rhs])
        return result

    @g.rule("oroperand = andoperand (AND andoperand)*")
    def visit_oroperand(self, node, (result, remaining)):
        while remaining:
            op, rhs = remaining.pop(0)
            result = Call(Attr(result, Name(self.aliases[op])), [rhs])
        return result

    @g.rule("andoperand = NOT? notoperand")
    def visit_andoperand(self, node, (not_, operand)):
        if not_:
            return Call(Attr(operand, Name(self.unary_aliases[not_[0]])), [])
        else:
            return operand


    @g.rule("notoperand = cmpoperand (cmpop cmpoperand)*")
    def visit_notoperand(self, node, (result, remaining)):
        while remaining:
            op, rhs = remaining.pop(0)
            result = Call(Attr(result, op), [rhs])
        return result

    @g.rule('cmpop = GE / LE / LT / GT / EQL / NEQ')
    def visit_cmpop(self, node, (op,)):
        return Name(self.aliases[op])

    @g.rule("cmpoperand = addoperand (addop addoperand)*")
    def visit_cmpoperand(self, node, children):
        result = children[0]
        remaining = children[1]
        while remaining:
            result = Call(Attr(result, remaining[0][0]), [remaining[0][1]])
            remaining.pop(0)
        return result

    @g.rule('addop = PLUS / MINUS')
    def visit_addop(self, node, (op,)):
        return Name(self.aliases[op])

    @g.rule("addoperand = muloperand (mulop muloperand)*")
    def visit_addoperand(self, node, children):
        result = children[0]
        remaining = children[1]
        while remaining:
            result = Call(Attr(result, remaining[0][0]), [remaining[0][1]])
            remaining.pop(0)
        return result

    @g.rule('mulop = MUL / DIV / MOD')
    def visit_mulop(self, node, (op,)):
        return Name(self.aliases[op])

    @g.rule("muloperand = uop? prim")
    def visit_muloperand(self, node, (uop, expr)):
        if uop:
            return Call(Attr(expr, uop[0]), [])
        else:
            return expr

    @g.rule('uop = MINUS / TWIDDLE')
    def visit_uop(self, node, (op,)):
        return Name(self.unary_aliases[op])

    @g.rule('prim = atom modifier*')
    def visit_prim(self, node, (atom, mods)):
        result = atom
        for m in mods:
            result = m(result)
        return result

    @g.rule('modifier = attrmod / callmod / getmod')
    def visit_modifier(self, node, (mod,)):
        return mod

    @g.rule('attrmod = DOT name')
    def visit_attrmod(self, node, (_, name)):
        class Mod:
            def __call__(self, expr):
                return Attr(expr, name)
            def assign(self, lhs, rhs):
                return Assign(Attr(lhs, name), rhs)
        return Mod()

    @g.rule('callmod = LPR exprs? RPR')
    def visit_callmod(self, node, (l, args, r)):
        if args:
            return lambda expr: Call(expr, args[0])
        else:
            return lambda expr: Call(expr, [])

    @g.rule('getmod = LBK exprs RBK')
    def visit_getmod(self, node, (l, args, r)):
        class Mod:
            def __call__(self, expr):
                return Call(Attr(expr, Name("__get__")), args)
            def assign(self, lhs, rhs):
                return ExprStmt(Call(Attr(lhs, Name("__set__")), args + [rhs]))
        return Mod()

    @g.rule('exprs = expr (COMMA expr)*')
    def visit_exprs(self, node, (first, rest)):
        return [first] + [n[-1] for n in rest]

    @g.rule('atom = literal / paren / super / new / var / native')
    def visit_atom(self, node, (atom,)):
        return atom

    @g.rule('paren = LPR expr RPR')
    def visit_paren(self, node, (l, expr, r)):
        return expr

    @g.rule('new = NEW type LPR exprs? RPR')
    def visit_new(self, node, (_, type, l, args, r)):
        if args:
            args = args[0]
        else:
            args = []
        return Call(type, args)

    @g.rule('var = name ""')
    def visit_var(self, node, (name, _)):
        return Var(name)

    @g.rule('super = SUPER ""')
    def visit_super(self, node, (s, _)):
        return Super()

    @g.rule('literal = number / string / list / map / null / bool')
    def visit_literal(self, node, (literal,)):
        return literal

    @g.rule('number = _ NUMBER _')
    def visit_number(self, node, (pre, number, post)):
        return Number(number)

    @g.rule(r'NUMBER = ~"[0-9]+(\.[0-9]+)?"')
    def visit_NUMBER(self, node, children):
        return node.text

    @g.rule('string = _ STRING _')
    def visit_string(self, node, (pre, string, post)):
        return String(string)

    @g.rule(r'STRING = ~"\"(\\\\[\"nrt\\\\]|\\\\u[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]|\\\\x[0-9a-fA-F][0-9a-fA-F]|[^\\\\\"])*\""')
    def visit_STRING(self, node, children):
        return node.text

    @g.rule('list = LBK exprs? RBK')
    def visit_list(self, node, (l, opt, r)):
        if opt:
            exprs = opt[0]
        else:
            exprs = []
        return List(exprs)

    @g.rule('map = LBR entries? RBR')
    def visit_map(self, node, (l, opt, r)):
        if opt:
            entries = opt[0]
        else:
            entries = []
        return Map(entries)

    @g.rule('null = NULL ""')
    def visit_null(self, node, (null, _)):
        return Null(null)

    @g.rule('bool = TRUE / FALSE')
    def visit_bool(self, node, (atom,)):
        return Bool(atom)

    @g.rule('entries = entry (COMMA entry)*')
    def visit_entries(self, node, (first, rest)):
        return [first] + [n[-1] for n in rest]

    @g.rule('entry = expr COLON expr')
    def visit_entry(self, node, (key, _, value)):
        return Entry(key, value)

    def flatten(self, stuff, result):
        for s in stuff:
            if isinstance(s, (Fixed, Var)):
                result.append(s)
            else:
                self.flatten(s, result)

    @g.rule('native = native_case+')
    def visit_native(self, node, cases):
        return Native(cases)

    @g.rule('native_case = _ "$" name_re? "{" stuff* "}" _')
    def visit_native_case(self, node, (ls, d, opt, l, stuff, r, rs)):
        if opt:
            name = opt[0]
        else:
            name = None
        flattened = []
        self.flatten(stuff, flattened)
        return NativeCase(name, flattened)

    @g.rule('stuff = fixed / dvar / braces')
    def visit_stuff(self, node, (stuff,)):
        return stuff

    @g.rule('fixed = ~"[^{$}]"+')
    def visit_fixed(self, node, children):
        return Fixed(node.text)

    @g.rule('dvar = "$" name_re')
    def visit_dvar(self, node, (_, name)):
        return Var(Name(name))

    @g.rule('braces = "{" stuff* "}"')
    def visit_braces(self, node, (l, stuff, r)):
        return Fixed("{"), stuff, Fixed("}")

    def visit_(self, node, children):
        return children

    @g.rule(r'_ = (~"[ \t\n\r]+" / ~"/\*.*?\*/"s / ~"//[^\n]*\n")*')
    def visit__(self, node, children): pass

del g

def rules():
    print Parser.rules
