# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from Shape import Shape

class Disk(Shape):
    """
    A representation of a circular disk
    """
    
    # interface
    def interior(self, point):
        """
        Predicate that checks whether {point} falls on my interior
        """
        r2 = self.radius**2
        x0, y0 = self.center
        x, y = point
        dx = x - x0
        dy = y - y0

        if dx*dx + dy*dy > r2:
            return False

        return True

    # meta methods
    def __init__(self, radius=1.0, center=(0.0, 0.0)): #@\label{line:disk:constructor}@
        self.radius = radius
        self.center = center
        return


# end of file 
