#
# label_selection_menu.py
#
# Copyright (C) 2014 Ratanak Lun <ratanakvlun@gmail.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Linking this software with other modules is making a combined work
# based on this software. Thus, the terms and conditions of the GNU
# General Public License cover the whole combination.
#
# As a special exception, the copyright holders of this software give
# you permission to link this software with independent modules to
# produce a combined work, regardless of the license terms of these
# independent modules, and to copy and distribute the resulting work
# under terms of your choice, provided that you also meet, for each
# linked module in the combined work, the terms and conditions of the
# license of that module. An independent module is a module which is
# not derived from or based on this software. If you modify this
# software, you may extend this exception to your version of the
# software, but you are not obligated to do so. If you do not wish to
# do so, delete this exception statement from your version.
#


import gtk

import labelplus.common.label
import labelplus.gtkui.common.gtklib

from labelplus.gtkui import RT


class LabelSelectionMenu(gtk.Menu):

  def __init__(self, model, on_activate=None, headers=True, root_items=[],
      sub_items=[]):

    super(LabelSelectionMenu, self).__init__()

    self._items = []
    self._menus = []

    self._build_menu(model, on_activate, headers, root_items, sub_items)

    self.show_all()

    del self._items
    del self._menus


  def get_label_item(self, id):

    def find_item(menu):

      for child in menu.get_children():
        name = child.get_name()

        if id == name:
          return child

        if id.startswith(name + ":"):
          submenu = child.get_submenu()
          if submenu:
            return find_item(submenu)
          else:
            return None

      return None


    return find_item(self)


  def _build_menu(self, model, on_activate, headers, root_items, sub_items):

    children = labelplus.gtkui.common.gtklib.treemodel_get_children(model)

    for child in list(children):
      id, data = model[child]
      if id in labelplus.common.label.RESERVED_IDS:
        children.remove(child)

    if root_items:
      self._items += labelplus.gtkui.common.gtklib.menu_add_items(self, -1,
        root_items)
      if children:
        self._items.append(labelplus.gtkui.common.gtklib.menu_add_separator(self))

    for child in children:
      self._create_item(model, child, self, on_activate, headers, sub_items)


  def _create_item(self, model, iter, menu, on_activate, headers, sub_items):

    id, data = model[iter]

    name = data["name"]

    item = gtk.MenuItem(name); RT.register(item, __name__)
    item.set_name(id)
    menu.append(item)
    self._items.append(item)

    children = labelplus.gtkui.common.gtklib.treemodel_get_children(model, iter)

    if not children and not sub_items:
      if on_activate:
        item.connect("activate", on_activate, id)
    else:
      submenu = gtk.Menu(); RT.register(submenu, __name__)
      item.set_submenu(submenu)
      self._menus.append(submenu)

      if headers:
        self._items += labelplus.gtkui.common.gtklib.menu_add_items(submenu, -1,
          (((gtk.MenuItem, name), on_activate, id),))
        self._items.append(labelplus.gtkui.common.gtklib.menu_add_separator(
          submenu))

      if sub_items:
        self._items += labelplus.gtkui.common.gtklib.menu_add_items(submenu, -1,
          sub_items, id)
        if children:
          self._items.append(labelplus.gtkui.common.gtklib.menu_add_separator(
            submenu))

      for child in children:
        self._create_item(model, child, submenu, on_activate, headers,
          sub_items)
