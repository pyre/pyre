// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import styles from './styles'


// the shape
const play = `
M 200 200
L 800 500
L 200 800
Z`


// render the shape
const shape = ({{ style }}) => {{
    // mix my paint
    const ico = {{ ...styles.icon, ...style?.icon }}

    // paint me
    return (
        <path d={{play}} style={{ico}} />
    )
}}


// publish
export default shape


// end of file
