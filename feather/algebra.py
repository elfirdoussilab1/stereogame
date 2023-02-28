from locale import normalize
import math
import numpy as np
import pygame

from feather.vector3 import Vec3


# creates a rotation matrix of angle (in degrees) around axis vec3(x,y,z)
from pygame.math import Vector3


def rotate(angle, x, y, z):
    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))
    magnitude = math.sqrt(x * x + y * y + z * z)
    nc = 1 - c

    x /= magnitude
    y /= magnitude
    z /= magnitude

    return np.array([
        [c + x ** 2 * nc, y * x * nc - z * s, z * x * nc + y * s, 0],
        [y * x * nc + z * s, c + y ** 2 * nc, y * z * nc - x * s, 0],
        [z * x * nc - y * s, z * y * nc + x * s, c + z ** 2 * nc, 0],
        [0, 0, 0, 1],
    ])


# creates a translation matrix of vec3(x,y,z)
def translate(x, y, z):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1],
    ])


# creates a scale matrix
def scale(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1],
    ])


def reflection(vector, n):
    vec = np.array([vector.x, vector.y, vector.z])
    normal = np.array([n.x, n.y, n.z])
    for i in range(3):
        vec[i] = -vec[i]
    ps = (vec[0] * normal[0] + vec[1] * normal[1] + vec[2] * normal[2])
    # return 2*ps*normal - vec
    res = [0, 0, 0]
    for i in range(3):
        res[i] = 2 * ps * normal[i] - vec[i]
    return Vec3(res[0], res[1], res[2])


# creates a lookat view matrix looking at center from eye with up-vector equal to Y axis
def lookat(eye, center):
    vec3eye = Vector3(eye.x, eye.y, eye.z)

    zaxis = center - vec3eye
    zaxis = zaxis.normalize()
    up = pygame.math.Vector3(0, 1, 0)

    xaxis = zaxis.cross(up).normalize()
    yaxis = xaxis.cross(zaxis).normalize()
    zaxis = -zaxis

    return np.array([
        [xaxis.x, xaxis.y, xaxis.z, -xaxis.dot(vec3eye)],
        [yaxis.x, yaxis.y, yaxis.z, -yaxis.dot(vec3eye)],
        [zaxis.x, zaxis.y, zaxis.z, -zaxis.dot(vec3eye)],
        [0, 0, 0, 1]
    ]).transpose().dot(scale(1, -1, 1))


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def applyMat4ToVector3(matrix, x, y, z):
    # returns the vector3 result of applying the matrix to the vector3 (x,y,z)
    return np.array([
        matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + matrix[0][3],
        matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + matrix[1][3],
        matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + matrix[2][3],
    ])
