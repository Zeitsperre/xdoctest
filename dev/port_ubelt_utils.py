"""
Statically ports utilities from ubelt needed by xdoctest.
"""


def _autogen_xdoctest_utils():
    import ubelt as ub

    # Uses netharn closer until it is ported to a standalone module
    import netharn as nh
    closer = nh.export.closer.Closer()

    from ubelt import util_import
    closer.add_dynamic(util_import.split_modpath)
    closer.add_dynamic(util_import.modpath_to_modname)
    closer.add_dynamic(util_import.modname_to_modpath)
    closer.add_dynamic(util_import.import_module_from_name)
    closer.add_dynamic(util_import.import_module_from_path)
    closer.add_dynamic(util_import._pkgutil_modname_to_modpath)
    closer.add_dynamic(util_import._importlib_import_modpath)
    closer.add_dynamic(util_import.is_modname_importable)

    closer.expand(['ubelt'])
    text = closer.current_sourcecode()
    print(text)

    import redbaron
    new_baron = redbaron.RedBaron(text)
    new_names = [n.name for n in new_baron.node_list if n.type in ['class', 'def']]

    import xdoctest
    old_baron = redbaron.RedBaron(open(xdoctest.utils.util_import.__file__, 'r').read())

    old_names = [n.name for n in old_baron.node_list if n.type in ['class', 'def']]

    set(old_names) - set(new_names)
    set(new_names) - set(old_names)

    prefix = ub.codeblock(
        '''
        # -*- coding: utf-8 -*-
        """
        This file was autogenerated based on code in ubelt
        """
        from __future__ import print_function, division, absolute_import, unicode_literals
        ''')

    fpath = ub.expandpath('~/code/xdoctest/xdoctest/utils/util_import.py')
    open(fpath, 'w').write(prefix + '\n' + text + '\n')
