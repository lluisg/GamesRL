# -*- coding: utf-8 -*-

import os

class Piece(object):
    def __init__(self, tipo=0, visible=False, found=False):
        self.setValue(tipo)
        self.setVisible(visible)
        self.setFound(found)

    def setValue(self, tipo):
        self.tipo = tipo

    def getValue(self):
        return self.tipo

    def setVisible(self, visible):
        self.visible = visible

    def getVisible(self):
        return self.visible

    def setFound(self, found):
        self.found = found

    def getFound(self):
        return self.found

