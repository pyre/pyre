# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from Shape import Shape

class Disk(Shape):
    """
    A representation of a circular disk
    """

    # interface
    def interior(self, points):
        """
        Predicate that filters out points that are not in my interior
        """
        r2 = self.radius**2
        x0, y0 = self.center

        for x,y in points: #@\label{line:circle:generators:loop}@
            dx = x - x0
            dy = y - y0
            if dx*dx + dy*dy <= r2:
                yield 1 #@\label{line:circle:generators:true}@

        return #@\label{line:circle:generators:return}@


    # meta methods
    def __init__(self, radius=1.0, center=(0.0, 0.0)):
        self.radius = radius
        self.center = center
        return


# end of file 
