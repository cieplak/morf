import collections

import addict


class Path(collections.namedtuple('Path', ['string', 'list'])):

    separator = '/'

    @classmethod
    def parse(cls, path_string):
        if path_string[0] != cls.separator:
            raise ValueError('Invalid path: %s' % path_string)
        return cls(path_string, path_string[1:].split(cls.separator))

    def resolve(self, dictionary):
        if self.string == self.separator:
            return dictionary
        try:
            value = reduce(dict.get, self.list, dictionary)
        except Exception:
            raise Exception('Could not resolve path %s in %s' % (self, dictionary))
        return value

    def set(self, dictionary, value):
        branch, leaf = (
            self.list[:-1], self.list[-1]
        )
        tmp_dictionary = addict.Dict(dictionary)
        if self.string == '/':
            node = tmp_dictionary
        else:
            node = reduce(getattr, branch, tmp_dictionary)

        if leaf:
            setattr(node, leaf, value)
        else:
            if isinstance(value, collections.Mapping):
                node.update(value)
            else:
                raise Exception(
                    'Cannot overwrite the branch at %s with the leaf value %s' %
                    (self.string, value)
                )
        dictionary_copy = tmp_dictionary.to_dict()
        del tmp_dictionary
        return dictionary_copy
