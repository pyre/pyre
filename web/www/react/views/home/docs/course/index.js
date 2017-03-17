// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
import { Switch, Route, Link } from 'react-router-dom'

// support
import { Pyre, Section, Subsection, Paragraph } from 'widgets/doc'

// locals
import styles from './styles'
import Syllabus from './Syllabus'
import Overview from './overview'

// dress up the section title as a link to the syllabus
const title = (
    <span>A short course on <Pyre/></span>
)

// declaration
const Course = () => (
    <Section id="syllabus" style={styles.container} title={title}>
        <Switch>
            <Route path="/docs/course/overview" component={Overview} />
            {/* by default, show the syllabus */}
            <Route path="/docs/course" component={Syllabus} />
        </Switch>
    </Section>
)

//   publish
export default Course

// end of file
