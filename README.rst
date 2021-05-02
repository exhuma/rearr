rearr
=====

rearr will rearrage Python modules and classed by type and alphabetically.

This will very likely break the code, so use at your own risk. This has not yet
been battle tested and should not be assumed "production ready". Make sure you
have backups or revision control before applying it to any file.


Example
=======

Before
------

::

    """
    Hello
    """
    from functools import lru_cache


    def foo(f):
        return f


    def myfun3():
        pass


    def _myprifun():
        pass


    def __morepriv():
        pass


    class ClsWithoutDocString:
        def foo(self):
            pass


    class ClsWithParent(ClsWithoutDocString):
        pass


    # Comment above "MyClass"
    # second line of comment above "MyClass"
    class MyClass:
        """
        docstring of "MyClass"
        """

        def meth(self):  # eol-comment after MyClass.meth()
            pass

        def __init__(self) -> None:
            pass

        def meth3(self):
            pass

        @lru_cache
        def meth22(self):
            pass

        def meth2(self):
            pass

        @classmethod
        @lru_cache
        @foo
        def cm(cls):
            pass

        @staticmethod
        def sm():
            pass

        @classmethod
        def cm2(cls):
            pass


    def myfun2():
        pass


    def myfun1():
        pass


After (sorted but broken)
-------------------------

::

    """
    Hello
    """
    from functools import lru_cache


    class ClsWithParent(ClsWithoutDocString):
        pass


    class ClsWithoutDocString:
        def foo(self):
            pass


    # Comment above "MyClass"
    # second line of comment above "MyClass"
    class MyClass:
        """
        docstring of "MyClass"
        """

        @staticmethod
        def sm():
            pass

        @classmethod
        @lru_cache
        @foo
        def cm(cls):
            pass

        @classmethod
        def cm2(cls):
            pass

        @lru_cache
        def meth22(self):
            pass

        def __init__(self) -> None:
            pass

        def meth(self):  # eol-comment after MyClass.meth()
            pass

        def meth2(self):
            pass

        def meth3(self):
            pass


    def __morepriv():
        pass


    def _myprifun():
        pass


    def foo(f):
        return f


    def myfun1():
        pass


    def myfun2():
        pass


    def myfun3():
        pass
