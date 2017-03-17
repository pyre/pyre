// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
import { Link } from 'react-router-dom'

// support
import { Pyre, Section, Subsection, Paragraph } from 'widgets/doc'
// locals
import styles from './styles'

// declaration
const Syllabus = () => (
    <Section id="docs" title="Documentation">

        <Paragraph>
        </Paragraph>

        <Subsection title="Syllabus">
            <ul>
                <li><Link to="docs/overview">overview</Link></li>
            </ul>
        </Subsection>

    </Section>
)

//   publish
export default Syllabus

// end of file
