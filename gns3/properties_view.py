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


from .qt import QtWidgets
from .properties import Properties


class PropertiesView(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.refresh()

    def refresh(self):
        properties = Properties.instance()
        widget = QtWidgets.QWidget(self.parent())
        form = QtWidgets.QFormLayout()


        for section, props in properties.nodeProperties().items():
            title = QtWidgets.QLabel(section)
            form.addWidget(title)

            for prop in props:
                label = QtWidgets.QLabel(prop['name'] + ': ' , widget)
                edit = QtWidgets.QLineEdit(widget)
                if prop['type'] == 'ipv4':
                    edit.setInputMask('000.000.000.000;_')
                form.addRow(label, edit)

        save = QtWidgets.QPushButton("Apply", self)
        save.clicked.connect(self._saveButtonClickedSlot)

        form.addWidget(save)

        widget.setLayout(form)
        self.setWidget(widget)

    def _saveButtonClickedSlot(self):
        42 / 0
