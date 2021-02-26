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
import {{ Help }} from '~/shapes'
// styles
import styles from './styles'


// show the embedded documentation
const activity = ({{ size, style }}) => {{
    // paint me
    return (
        <Activity size={{size}} url="/help" barStyle={{style}} style={{styles}} >
            <Help />
        </Activity >
    )
}}


// publish
export default activity


// end of file
