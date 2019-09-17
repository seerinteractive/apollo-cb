#standard
from collections import UserDict
from collections import UserList
import typing

#third party
import attr
from attr.validators import instance_of

#local
from apollo.builder.exceptions import MethodError
from apollo.builder.exceptions import NestedFoldersForbidden
from apollo.builder.exceptions import ListAsValueRequired
from apollo.builder.exceptions import MoreThanOneKeySupplied
from apollo.builder.exceptions import OnlyStringsOrIntsAllow
from apollo.builder.exceptions import DelimiterMustBeString


@attr.s
class DictConverter(UserDict):

    
    dynamic = attr.ib(default = {}, validator = instance_of(dict))
    static = attr.ib(default = {}, validator = instance_of(dict))    

    @dynamic.validator
    def dynamic_validator(self, attribute, value):

        for val in value.values():
            if not isinstance(val, list):
                raise ListAsValueRequired(
                    "Use a list as a value in dictionary, e.g. {'a': [1,2,3]}"
                )

        if len(value) > 1:
            raise MoreThanOneKeySupplied(
                f"Please supply only one key. {len(value)} keys were given"
            )

    @static.validator
    def static_validator(self, attribute, value):
        for val in value.values():
            if not isinstance(val, (int, str)):
                raise OnlyStringsOrIntsAllow(
                    "Only value strings or ints allowed in dictionary, e.g. {'a': '3'}, not {'a': [1,2,3]}"
                )


    @property
    def combined(self):

        list_a = self.static
        list_b = self.dynamic

        combined = {}

        combined.update(list_a)
        combined.update(list_b)

        return combined

    @property
    def data(self):
        val = self.combined
        cnt = 0

        out = []

        for k, v in val.items():

            if isinstance(v, zip) and isinstance(k, tuple):
                z = list(zip(k, v))

                for m in z:
                    w, v = m
                    v, *_ = v

                    for f in v:
                        param = {}
                        p = val.copy()
                        del p[k]
                        param.update({w: f})
                        param.update(p)
                        cnt += 1
                        out.append(param)
                        # yield param

            elif isinstance(v, list):
                for f in v:
                    param = {}
                    p = val.copy()
                    del p[k]
                    param.update({k: f})
                    param.update(p)
                    cnt += 1
                    out.append(param)
                    # yield param
        if cnt == 0:
            out.append(val)
            # yield val
        return out

def convert_to_str(val):
    if isinstance(val, (str, int)):
        return [val]
    elif val == None:
        return ['']
    else:
        return val

@attr.s
class ListConverter(UserList):

    static = attr.ib(converter = convert_to_str)  
    dynamic = attr.ib(default = attr.Factory(list), validator = instance_of((list)))
    delimiter = attr.ib(default = '/', converter = attr.converters.optional(str))
    
    @delimiter.validator
    def delimiter_validator(self,  attribute, value):

        if not isinstance(value, str):
            raise DelimiterMustBeString(
                f"Please use a str type. Instead of {value}"
            )

    @static.validator
    def static_validator(self, attribute, value):

        if ListConverter.count_lists(value) > 0:
            raise NestedFoldersForbidden("Please ensure you do not nest folders")

    @dynamic.validator
    def dynamic_validator(self,  attribute, value):
        if ListConverter.count_lists(value) > 0:
            raise NestedFoldersForbidden("Please ensure you do not nest folders")


    @property
    def combined(self):

        static = self.static.copy()
        dynamic = self.dynamic.copy()
        combined = static

        combined.extend([dynamic])
        return combined

    @staticmethod
    def count_lists(lists):
        count = 0
        for l in lists:
            if isinstance(l, (list, tuple)):
                count += 1
        return count

    @property
    def data(self):
        vals = self.combined
        cnt = 0
        to_str = lambda x: [str(i) for i in x if i]
        out = []
        for n, val in enumerate(vals):
            if isinstance(val, (list, range)):
                for f in val:
                    row = []
                    row.extend(vals[:n])
                    row.extend([f])
                    row.extend(vals[n + 1 :])
                    cnt += 1
                    out.append("/".join(to_str(row)))
        if cnt == 0:
            out.append(f"{self.delimiter}".join(to_str(vals)))
        return out