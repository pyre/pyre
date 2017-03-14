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
const SectionTitle = ({children, style}) => (
    <div style={section.bar}>
        <h1 style={{...section.title, ...style}}>
            {children}
        </h1>
        <img style={section.logo} src="graphics/logo.png" />
    </div>
)

// publish
export default SectionTitle

// end of file
