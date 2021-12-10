// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
import {{ graphql, useLazyLoadQuery }} from 'react-relay/hooks'

// locals
import styles from './styles'


// display the server state
const server = ({{style, ...props}}) => {{
    // the query fragment i care about
    const {{ version: {{major, minor, micro, revid}} }} = useLazyLoadQuery(query)

    // merge the overall styles
    const base = {{...style.box, ...styles.box, ...style.text, ...styles.text}}
    // and the state colorization
    const good = {{...style.status.good, ...styles.status.good}}

    // get the time
    const now = new Date()
    // use it to make a timestamp
    const title = `last checked on ${{now.toString()}}`

    // mark
    console.log(`server: ${{title}}`)

    // build the component and return it
    return (
        <div style={{{{...base, ...good}}}} title={{title}}>
            {project.name} server {{major}}.{{minor}}.{{micro}} rev {{revid}}
        </div>
    )
}}


// the query
const query = graphql`query serverQuery {{
    version {{
        major
        minor
        micro
        revid
    }}
}}`


// publish
export default server


// end of file
