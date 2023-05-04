// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'

// locals
// hooks
import {{ useEvent }} from '~/hooks'
// context
import {{ Provider }} from './context'
// hooks
import useFlex from './useFlex'
import useEndFlex from './useEndFlex'
import useDirection from './useDirection'
// styles
import styles from './styles'


const Box = ({{ style, children }}) => {{
    // get the flexbox direction
    const {{ direction }} = useDirection()
    // get the flex support
    const {{ endFlex }} = useEndFlex()
    const {{ flexingPanel, separatorLocation, doFlex }} = useFlex()

    // make a ref for my container
    const ref = React.useRef(null)
    // install our event listeners
    useEvent({{ name: "mouseup", listener: endFlex, client: ref }})
    useEvent({{ name: "mouseleave", listener: endFlex, client: ref }})
    useEvent({{
        name: "mousemove", listener: doFlex, client: ref,
        triggers: [flexingPanel, separatorLocation]
    }})

    // mix my paint
    const boxStyle = {{ ...styles.box, ...style?.box, flexDirection: direction }}

    // paint me
    return (
        <div ref={{ref}} style={{boxStyle}}>
            {{children}}
        </div>
    )
}}


// turn flex into a context provider and publish
export default ({{ direction, ...rest }}) => {{
    // set up the context provider
    return (
        <Provider direction={{direction}} >
            <Box {{...rest}} />
        </Provider >
    )
}}


// end of file
