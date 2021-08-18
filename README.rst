rearr
=====

rearr will rearrage Python modules and classed by type and alphabetically.

This will **very likely** break the code, so use at your own risk. This has not
yet been battle tested and should not be assumed "production ready". Make sure
you have backups or revision control before applying it to any file.

As of version 0.2.0, rearranging *only* takes place for files or classes
containing the ``# rearr: enable`` top-evel comment. This makes it "opt-in" to
avoid completely nuking the code-base.

Additionally, it now only checks if something *would* be done by default. To
overwrite files, the ``-w`` argument must be supplied. It will also
automatically keep backups of original files.

The backups can be disabled using ``--no-backup`` which might make sense in
projects using revision control.


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
