// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import styles from './styles'


// a stylable shimmy
const spacer = ({{ style }}) => {{
    // mix my styles
    const spacerStyle = {{ ...styles, ...style }}

    // paint me
    return (
        <div style={{spacerStyle}} />
    )
}}


// publish
export default spacer


// end of file
