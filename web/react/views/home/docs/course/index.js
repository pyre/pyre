// -*- web -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
import React from 'react'
import { Switch, Route, Link } from 'react-router-dom'

// support
import { Pyre, Subsection, Paragraph } from 'widgets/doc'

// locals
import styles from './styles'
import Syllabus from './Syllabus'
import Overview from './overview'

// declaration
const Course = () => (
    <Switch>
        <Route path="/docs/course/overview" component={Overview} />
        {/* by default, show the syllabus */}
        <Route path="/docs/course" component={Syllabus} />
    </Switch>
)

//   publish
export default Course

// end of file
