// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
// locals
import document from './styles'

// render
const TableOfContents = ({children}) => (
    <section style={document.toc.table}>
        <span style={document.toc.title}>Contents</span>
        {children}
    </section>
)

// defaults
TableOfContents.defaultProps = {
}

// publish
export default TableOfContents

// end of file
