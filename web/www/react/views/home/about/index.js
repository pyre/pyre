// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'

// locals
import styles from './styles'

// declaration
const About = () => (
    <section style={styles.section}>
        <h1 style={styles.title}>about</h1>
        <p style={styles.body}>
          <span className="pyre">pyre</span> is an open source application framework written
          in <a href="http://www.python.org">python</a>. It's an attempt to bring state of the
          art software design practices to scientific computing. The goal is to provide a
          strong skeleton on which to build scientific codes by steering the implementation
          towards usability and maintainability.
        </p>
        <p style={styles.body}>
          The basic conceptual building block in <span className="pyre">pyre</span> is
          the <em>component</em>. Components are classes that specifically grant access to some
          of their state to the application end user. Component authors provide default
          values to be used in case the user doesn't make a choice, but the user is explicitly
          given complete control and can override them during component configuration.
        </p>
    </section>
)

//   publish
export default About

// end of file
