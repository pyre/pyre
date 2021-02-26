// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
import {{ Colophon, Server, Spacer }} from '~/widgets'
// locals
import styles from './styles'


// the bar at the bottom of every page
const status = () => (
    // the container
    <footer style={{styles.box}}>

        {{/* version info and status of the app server */}}
        <Server style={{styles.server}}/>

        {{/* render a separator */}}
        <Spacer style={{styles.spacer}} />

        {{/* the box with the copyright note */}}
        <Colophon author="Michael&nbsp;Aïvázis" link="https://github.com/aivazis"
                  span="{project.span}"
                  style={{styles.colophon}} />

    </footer>
)


// publish
export default status


// end of file
