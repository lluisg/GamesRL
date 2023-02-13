# -*- coding: utf-8 -*-

import os

class Ficha(object):
    def __init__(self, tipo):
        self.setTipo(tipo)

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo


