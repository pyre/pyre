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
import {{ Skull }} from '~/shapes'
// styles
import styles from './styles'


// kill the server
const activity = ({{ size, style }}) => {{
    // paint me
    return (
        <Activity size={{size}} url="/stop" barStyle={{style}} style={{styles}} >
            <Skull />
        </Activity >
    )
}}


// publish
export default activity


// end of file
