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
const Content = ({title, children}) => (
    <div style={document.toc.item}>
        {title}
        {children}
    </div>
)

// defaults
Content.defaultProps = {
    title: null,
}

// publish
export default Content

// end of file
