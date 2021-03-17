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
import {{ Hammer }} from '~/shapes'
// styles
import styles from './styles'


// sandbox for experimenting with new features
const activity = ({{ size, style }}) => {{
    // paint me
    return (
        <Activity size={{size}} url="/experiment" barStyle={{style}} style={{styles}} >
            <Hammer />
        </Activity >
    )
}}


// publish
export default activity


// end of file
