// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
// locals
import { section } from './styles'

// render
const Section = ({children, style}) => (
    <section style={{...section.container, ...style}}>
        {children}
    </section>
)

// publish
export default Section

// end of file
