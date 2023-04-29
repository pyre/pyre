// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import styles from './styles'


// the area
const stop = (props) => {{
    // ask the server to shut down
    fetch('/stop').catch(
        // swallow any errors
        (error) => null
    )

    // the container
    return (
        <section style={{styles.stop}}>
            <div style={{styles.placeholder}}>
                <a href="/">{project.name}</a> has shut down; please close this window
            </div>
        </section>
    )
}}


// publish
export default stop


// end of file
