// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'

// support
import { Pyre, Section, Subsection, Paragraph } from 'widgets/doc'

// locals
import styles from './styles'

// declaration
const Overview = () => (
    <Section id="overview"
             style={styles.container}
             title={<span>Overview of <Pyre/></span>} >
    </Section>
)

//   publish
export default Overview

// end of file
