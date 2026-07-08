// -*- web -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
import React from 'react'
// locals
import document from './styles'

// render
const Content = ({title, children}) => (
    <div style={document.toc.item}>
        {title}
        <div style={document.toc.contents}>
            {children}
        </div>
    </div>
)

// defaults
Content.defaultProps = {
    title: null,
}

// publish
export default Content

// end of file
