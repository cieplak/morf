from .path import Path


class Morphism(object):

    def __init__(self, arrows):
        self.arrows = arrows

    def __call__(self, domain):
        codomain = {}
        for arrow in self.arrows:
            codomain = arrow.apply(domain, codomain)
        return codomain

    @classmethod
    def compile(cls, *expressions, **kwargs):
        ctx = kwargs.pop('ctx', {})
        arrows = [Arrow.parse(expr, ctx=ctx) for expr in expressions]
        return cls(arrows)


class Arrow(object):

    symbol = '->'

    def __init__(self, source_paths, function, destination_path):
        self.source_paths = source_paths
        self.function = function
        self.destination_path = destination_path

    @classmethod
    def parse(cls, representation, ctx=None):
        tokens = map(str.strip, representation.split(cls.symbol))

        destination_path = Path.parse(tokens.pop())
        source_paths = []

        callable_tokens = []
        for token in tokens:
            if token[0] == '/':
                source_paths.append(Path.parse(token))
            else:
                callable_tokens.append(token)
        callables = []
        for token in callable_tokens:
            if token in ctx:
                callables.append(ctx[token])
            elif token.startswith('py::'):
                try:
                    python_function = eval(token[4:])
                    if not callable(python_function):
                        raise Exception(
                            'Token %s is not a callable in expression %s' %
                            (token, representation)
                        )
                    callables.append(python_function)
                except Exception as e:
                    raise Exception(
                        'Failed to parse token %s in expression %s' %
                        (token, representation)
                    )
        function = cls.compose(*callables)
        return cls(source_paths, function, destination_path)

    def apply(self, domain, codomain):
        inputs = [path.resolve(domain) for path in self.source_paths]
        input_ = inputs[0] if len(inputs) == 1 else tuple(inputs)
        destination_value = self.function(input_)
        return self.destination_path.set(codomain, destination_value)

    @classmethod
    def compose(cls, *functions):
        def inner(arg):
            for f in functions:
                arg = f(arg)
            return arg
        return inner
