// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'

// support
import { Section, SectionTitle, Paragraph } from 'widgets/doc'
// locals
import styles from './styles'

import Ball from './Ball'
import Shape from './Shape'
import Gauss from './Gauss'


// declaration
const About = () => (
    <Section>

        <SectionTitle>about</SectionTitle>

        <Paragraph>
          <span className="pyre">pyre</span> is an open source application framework written
          in <a href="http://www.python.org">python</a>. It's an attempt to bring state of the
          art software design practices to scientific computing. The goal is to provide a
          strong skeleton on which to build scientific codes by steering the implementation
          towards usability and maintainability.
        </Paragraph>

        <Paragraph>
          The basic conceptual building block in <span className="pyre">pyre</span> is
          the <em>component</em>. Components are classes that specifically grant access to some
          of their state to the application end user. Component authors provide default
          values to be used in case the user doesn't make a choice, but the user is explicitly
          given complete control and can override them during component configuration.
        </Paragraph>

        <Paragraph>
            Here is a simple component that represents a multi-dimensional ball. It has two
            user-configurable properties, and a single method that computes its measure:
        </Paragraph>

        <Ball/>

        <Paragraph>
            Packages that support more than one kind of shape should probably declare
            a <em>protocol</em> to capture their basic properties and behaviors, much like
            abstract base classes do for their sub-classes.
        </Paragraph>

        <Shape/>

        <Paragraph>
            Then, applications can use the protocol to express a <em>requirement</em> for some
            kind of shape, and defer to the user for the actual choice. If the user does not
            express an opinion, the default specified by Shape will be used.
        </Paragraph>

        <Gauss/>

        <Paragraph>
            For details, and more examples, please take a look at the tutorials.
        </Paragraph>

    </Section>
)

//   publish
export default About

// end of file
