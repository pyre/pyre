// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
// locals
import { section }  from './styles'

// render
const Paragraph = ({children, style}) => (
    <p style={{...section.body, ...style}}>
        {children}
    </p>
)

// publish
export default Paragraph

// end of file
