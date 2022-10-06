import enum
from math import sqrt, pow
from constants import VERTICES, START_VERTICE_ROW, END_VERTICE_ROW, PIVOT_ROW, NEIGHBOURS, COLONY, ROADS, HARBOUR, Resource
from collections import namedtuple
from graph import Graph

def inner_product(*args):
    prod = [1]*len(args[0])
    for p in args:
        for i in (range(len(prod))):
            prod[i] *= p[i]
    return prod

def norm(p):
    return dist(p, (0,0))

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def squared_dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def dist(p1,p2):
    return sqrt(squared_dist(p1,p2))

def dot(*args):
    prod = inner_product(*args)
    return dist(prod, (0,0))
