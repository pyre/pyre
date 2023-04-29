// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'

// project
// hooks
import {{ useEvent }} from '~/hooks'
// locals
// context
import {{ Provider }} from './context'
// hooks
import useFlex from './useFlex'
import useEndFlex from './useEndFlex'
import useDirection from './useDirection'
// styles
import styles from './styles'


// the top level flexing container
const Flexbox = ({{ style, children, ...rest }}) => {{
    // get the flexbox direction
    const {{ direction }} = useDirection()
    // get the flex support
    const {{ endFlex }} = useEndFlex()
    const {{ flexingPanel, separatorLocation, doFlex }} = useFlex()

    // make a ref for my container
    const ref = React.useRef(null)

    // install my event listeners
    // end the flex when the user lets go of the mouse
    useEvent({{
        name: "mouseup", listener: endFlex, client: ref,
        triggers: [flexingPanel]
    }})
    // end the flex when the  mouse leaves my client area
    useEvent({{
        name: "mouseleave", listener: endFlex, client: ref,
        triggers: [flexingPanel]
    }})
    // flex when the mouse moves; the handler does something non-trivial only when there is
    // a flexing panel
    useEvent({{
        name: "mousemove", listener: doFlex, client: ref,
        triggers: [flexingPanel, separatorLocation]
    }})

    // mix my paint
    const boxStyle = {{ ...styles.box, ...style?.box, flexDirection: direction }}

    // paint me
    return (
        <div ref={{ref}} style={{boxStyle}} {{...rest}} >
            {{children}}
        </div >
    )
}}


// turn flex into a context provider and publish
export const Box = ({{ direction, ...rest }}) => {{
    // set up the context provider
    return (
        <Provider direction={{direction}} >
            <Flexbox {{...rest}} />
        </Provider >
    )
}}


// end of file
