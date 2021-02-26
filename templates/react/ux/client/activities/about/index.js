// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
import {{ Link }} from 'react-router-dom'

// locals
// widgets
import {{ Activity }} from '~/activities'
// my shape
import {{ Flame }} from '~/shapes'
// styles
import styles from './styles'


// visualize
const activity = ({{ size, style }}) => {{
    // paint me
    return (
        <Activity size={{size}} url="/about" barStyle={{style}} style={{styles}} >
            <Flame />
        </Activity >
    )
}}


// publish
export default activity


// end of file
