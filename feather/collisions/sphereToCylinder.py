from feather.algebra import dot
from math import sqrt
import numpy as np

"""Checks whereas the sphere collides with the given cylinder."""
def sphereToCylinder(sphere, cylinder):
    endPoint1 = cylinder.getEndPoint1()
    endPoint2 = cylinder.getEndPoint2()
    cylinderDirection = endPoint2 - endPoint1
    sphereCenter = np.array([sphere.position.x, sphere.position.y, sphere.position.z])

    distanceFactorFromEP1 = dot(sphereCenter - endPoint1, cylinderDirection) / dot(cylinderDirection, cylinderDirection)

    if(distanceFactorFromEP1 < 0):
        distanceFactorFromEP1 = 0
    elif(distanceFactorFromEP1 > 1):
        distanceFactorFromEP1 = 1

    closestPointOnCylinder = endPoint1 + cylinderDirection * distanceFactorFromEP1

    collisionPoint = sphereCenter - closestPointOnCylinder

    distance = sqrt(dot(collisionPoint, collisionPoint))

    return distance < sphere.getRadius() + cylinder.getRadius()