// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
// framework
import React from 'react'
// routing
import {{ Outlet }} from 'react-router-dom'

// locals
import styles from './styles'
// view
import {{ Status }} from '~/views'
// activities
import {{ ActivityBar }} from '~/activities'
// widgets
import {{ Flex }} from '~/widgets'


// the main app working area
// the layout is simple: the activity bar and activity dependent routing
const Panel = () => {{
    // lay out the main page
    return (
        <section style={{styles.page}} >
            <section style={{styles.panel}} >
                {{/* navigation bar */}}
                <ActivityBar style={{styles.activitybar}} />

                {{/* a flex container with two panels */}}
                <Flex.Box direction="row" style={{styles.flex}} >

                    {{/* the activity specific workarea */}}
                    <Flex.Panel min={{400}} auto={{true}} style={{styles.flex}} >
                        {{/* render whatever the router hands me */}}
                        <Outlet />
                    </Flex.Panel>

                </Flex.Box>
            </section >
            <Status />
        </section >
    )
}}


// publish
export default Panel


// end of file
