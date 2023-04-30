// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
import {{ useLocation }} from 'react-router-dom'
// locals
// shapes
import {{ Hammer }} from '~/shapes'
// styles
import styles from './styles'


// the area
export const NYI = () => {{
    // grab the location
    const location = useLocation()

    // render
    return (
        <section style={{styles.nyi}}>
            <div style={{styles.placeholder}}>
                <svg style={{styles.icon}} version="1.1" xmlns="http://www.w3.org/2000/svg">
                    <g transform="scale(0.3)" fill="#f37f19" stroke="none">
                        <Hammer style={{styles.shape}} />
                    </g>
                </svg>
                <p style={{styles.message}}>
                    <span style={{styles.location}}>{{location.pathname}}</span>
                    &nbsp;is not implemented yet
                </p>
            </div>
        </section>
    )
}}


// end of file
