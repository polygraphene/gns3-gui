#!/usr/bin/env python
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import copy

from .qt import QtWidgets
from .properties import Properties
from .items.node_item import NodeItem


class PropertiesView(QtWidgets.QDockWidget):
    """
    Allow user to edit node properties.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self._properties_widgets = []
        self._selected_nodes = []

        parent.uiGraphicsView.scene().selectionChanged.connect(self._sceneSelectionChangedSlot)
        self.refresh()

    def _sceneSelectionChangedSlot(self):
        """
        Called when a new item in selected in the topology
        """
        self._selected_nodes = []
        for item in self.parent().uiGraphicsView.scene().selectedItems():
            if isinstance(item, NodeItem):
                self._selected_nodes.append(item.node())
        self.refresh()

    def refresh(self):
        widget = QtWidgets.QWidget(self.parent())
        self.setWidget(widget)

        node = self.getSelectedNode()
        if node is None:
            return
        node_settings = node.settings()

        properties = Properties.instance()
        form = QtWidgets.QFormLayout()
        widget.setLayout(form)

        self._properties_widgets = []

        for section, props in properties.nodeProperties().items():
            title = QtWidgets.QLabel(section)
            form.addWidget(title)

            for prop in props:
                label = QtWidgets.QLabel(prop['name'] + ': ' , widget)
                edit = QtWidgets.QLineEdit(widget)
                if prop['type'] == 'ipv4':
                    edit.setInputMask('000.000.000.000;_')
                if prop['key'] in node_settings:
                    edit.setText(node_settings[prop['key']])

                prop = copy.copy(prop)
                prop['widget'] = edit

                self._properties_widgets.append(prop)
                form.addRow(label, edit)

        save = QtWidgets.QPushButton('Apply', self)
        save.clicked.connect(self._saveButtonClickedSlot)
        form.addWidget(save)

    def getSelectedNode(self):
        """
        Get currently selected node or None if zero or more than one node is selected
        """
        if len(self._selected_nodes) == 0 or len(self._selected_nodes) > 1:
            return None
        return self._selected_nodes[0]

    def _saveButtonClickedSlot(self):
        node = self.getSelectedNode()

        new_settings = {}

        for prop in self._properties_widgets:
            widget = prop['widget']
            if isinstance(widget, QtWidgets.QLineEdit):
                value = widget.text()
                new_settings[prop['key']] = value

        node.update(new_settings)
