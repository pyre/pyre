// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
// context
import {{ Context }} from './context'


// grant access to the flexbox direction
export default () => {{
    // pull the values from the context
    const {{ direction, isRow, parity }} = React.useContext(Context)
    // and make them available
    return {{ direction, isRow, parity }}
}}


// end of file
