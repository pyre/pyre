// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'

// locals
// hooks
import useDirectionalAttributes from './useDirectionalAttributes'
// styles
import styles from './styles'

// the separator inserted between consecutive items in a flex panel
const separator = ({{ beginFlex, style }}) => {{
    // access the flex direction
    const {{ mainExtent, crossExtent, transform, cursor }} = useDirectionalAttributes()

    // direction dependent settings
    // for the rule
    let dirRuleStyle = {{
        cursor,
        [mainExtent]: "1px"
    }}
    // for the handle
    let dirHandleStyle = {{
        transform,
        [mainExtent]: "9px",
        [crossExtent]: "100%",
    }}

    // mix my paint
    const ruleStyle = {{ ...styles.separator.rule, ...dirRuleStyle, ...style?.rule }}
    // the paint of my handle
    const handleStyle = {{ ...styles.separator.handle, ...dirHandleStyle, ...style?.handle }}
    // and the state dependent coloring
    const stateStyle = {{ ...styles.separator.colors, ...style?.colors }}

    // make a ref for the handle
    const ref = React.useRef(null)

    // when the mouse enters my space
    const onMouseEnter = (evt) => {{
        // stop this event from bubbling up
        evt.stopPropagation()
        // get the handle
        const handle = ref.current
        // if the handle has rendered
        if (handle) {{
            // paint it
            handle.style.backgroundColor = stateStyle.visible
        }}
        // all done
        return
    }}

    // when the mouse leaves my space
    const onMouseLeave = (evt) => {{
        // stop this event from bubbling up
        evt.stopPropagation()
        // quash any side effects
        evt.preventDefault()
        // get the handle
        const handle = ref.current
        // if the handle has rendered
        if (handle) {{
            // paint it
            handle.style.backgroundColor = stateStyle.hidden
        }}
        // all done
        return
    }}

    // assemble the handle controls
    const handleControls = {{
        onMouseEnter,
        onMouseLeave,
        onMouseDown: beginFlex,
    }}

    // paint me
    return (
        <div style={{ruleStyle}} >
            <div ref={{ref}} style={{handleStyle}} {{...handleControls}} />
        </div>
    )
}}


// publish
export default separator


// end of file
