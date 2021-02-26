// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import styles from './styles'


// the flame data
const flame = `
M 470.1332 8
C 798.1332 254 -267.8668 532.8 338.9332 992
C 207.73322 696.8 437.3332 565.6 453.7332 565.6
C 404.5332 860.8 568.5332 746 584.9332 942.8
C 666.9332 860.8 666.9332 828 650.5332 795.2
C 732.5332 860.8 716.1332 893.6 699.7332 992
C 814.5332 893.6 929.3332 696.8 781.7332 450.8
C 781.7332 549.2 765.3332 598.4 666.9332 664
C 716.1332 598.4 863.7332 188.4 470.1332 8
Z`


// render the shape
const shape = ({{ style }}) => {{
    // mix my paint
    const ico = {{ ...styles.icon, ...style?.icon }}

    // paint me
    return (
        <path d={{flame}} style={{ico}} />
    )
}}


// publish
export default shape


// end of file
