// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import styles from './styles'


// a container with author and copyright notes
const colophon = ({{ author, link, span, style }}) => {{
    // mix my styles
    const boxStyle = {{ ...styles.box, ...style?.box }}
    const copynoteStyle = {{ ...styles.copyright, ...style?.copyright }}
    const authorStyle = {{ ...styles.author, ...style?.author }}

    // paint me
    return (
        <div style={{boxStyle}}>
            <span style={{copynoteStyle}}>
                {{span}}
                &nbsp;
                &copy;
                &nbsp;
                <a style={{authorStyle}} href={{link}}>
                    {{author}}
                </a>
            </span>
        </div>
    )
}}


// publish
export default colophon


// end of file
