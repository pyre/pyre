// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
// shapes
import {{ Flame }} from '~/shapes'
// styles
import styles from './styles'


// the area
const loading = () => (
    <section style={{styles.loading}}>
        <div style={{styles.placeholder}}>
            <svg style={{styles.logo}} version="1.1" xmlns="http://www.w3.org/2000/svg">
                <g transform=" scale(.3)" >
                    <Flame style={{styles.shape}} />
                </g>
            </svg>
            <p style={{styles.message}}>
                loading; please wait<a href="/stop">...</a>
            </p>
        </div>
    </section>
)


// publish
export default loading


// end of file
