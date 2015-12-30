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


class Properties:
    def __init__(self):
        self._node_properties = {}

        self.registrerNodeProperties("General", "asn", "ASN")
        self.registrerNodeProperties("Addressing", "ipv4.subnet", "IPV4 subnet", type="ipv4")

    def nodeProperties(self):
        return self._node_properties

    def registrerNodeProperties(self, section, key, name, type="string"):
        self._node_properties.setdefault(section, [])
        prop = {
            "key": key,
            "name": name,
            "type": type
        }
        self._node_properties[section].append(prop)

    @staticmethod
    def instance():
        """
        Singleton to return only on instance of Properties.
        :returns: instance of Properties
        """

        if not hasattr(Properties, '_instance') or Properties._instance is None:
            Properties._instance = Properties()
        return Properties._instance

