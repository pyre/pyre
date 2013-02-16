#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access the framework
import pyre


# declare an abstract specification
class task(pyre.protocol, family='toy.tasks'):

    # types
    from pyre.units.time import hour

    # public state
    duration = pyre.properties.dimensional(default=1*hour)

    # interface
    @pyre.provides
    def perform(self):
        """do something"""

    # framework support
    @classmethod
    def pyre_default(cls):
        return relax


# the base class for task implementors
class activity(pyre.component, implements=task):

    duration = pyre.properties.dimensional(default=1*task.hour)

    @pyre.export
    def perform(self):
        return '{0.description} for {0.duration:base={hour},label=hour|hours}'.format(
            self, hour=task.hour)


# an actual task
class relax(activity, family='toy.tasks.relax'):

    description = 'relaxing'


# another actual task
class study(activity, family='toy.tasks.study'):

    description = 'studying'
    duration = pyre.properties.dimensional(default=2*task.hour)
    

class patrol(activity, family='toy.tasks.patrol'):

    description = 'patrolling'
    duration = pyre.properties.dimensional(default=1.5*task.hour)
    

# a specification for people categories
class people(pyre.protocol, family='toy.people'):

    activities = pyre.properties.list(schema=task())

    @pyre.provides
    def perform(self):
        """perform my specified activities"""


# an actual person category
class person(pyre.component, implements=people):

    activities = pyre.properties.list(schema=task())

    @pyre.export
    def perform(self):
        """perform my activities"""
        for activity in self.activities: yield activity.perform()


# students
class student(person, family='toy.people.student'):

    foo = task()
    activities = pyre.properties.list(schema=task(default=relax))


# policemen
class policeman(person, family='toy.people.policeman'):

    activities = pyre.properties.list(schema=task(default=patrol))


# end of file 
