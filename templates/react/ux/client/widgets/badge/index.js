// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import styles from './styles'


// a button with an SVG image as content
const badge = ({{ name, size, state, style, children }}) => {{
    // make local state for the extra styling of the badge and the shape necessary when
    // questioning whether the activity is available
    const [extraBadgeStyle, setBadgeStyle] = React.useState(null)
    const [extraShapeStyle, setShapeStyle] = React.useState(null)

    // mix my paint
    // for the badge
    const badgeStyle = {{
        // the base styling
        ...styles.badge, ...style?.badge,
        // if i'm disabled
        ...(state === "disabled" ? styles.disabled.badge : {{}}),
        ...(state === "disabled" ? style?.disabled.badge : {{}}),
        // if i'm engaged
        ...(state === "engaged" ? styles.engaged.badge : {{}}),
        ...(state === "engaged" ? style?.engaged.badge : {{}}),
        // and whatever the extra styling says
        ...extraBadgeStyle,
    }}

    // for the shape
    const shapeStyle = {{
        // the base styling
        ...styles.shape, ...style?.shape,
        // if i'm disabled
        ...(state === "disabled" ? styles.disabled.shape : {{}}),
        ...(state === "disabled" ? style?.disabled.shape : {{}}),
        // if i'm engaged
        ...(state === "engaged" ? styles.engaged.shape : {{}}),
        ...(state === "engaged" ? style?.engaged.shape : {{}}),
        // and whatever the extra styling says
        ...extraShapeStyle,
    }}

    // support for questioning whether i'm available
    let controls = {{}}
    // if i'm not disabled
    if (state !== "disabled") {{
        // make a function that can highlight the badge and the shape
        const highlight = () => {{
            // mix the highlight styles
            const badgeStyle = {{ ...styles.available.badge, ...style?.available.badge }}
            const shapeStyle = {{ ...styles.available.shape, ...style?.available.shape }}
            // and apply them
            setBadgeStyle(badgeStyle)
            setShapeStyle(shapeStyle)
            // all done
            return
        }}

        // make a function that resets the highlight
        const reset = () => {{
            // by removing any extra styling
            setBadgeStyle(null)
            setShapeStyle(null)
            // all done
            return
        }}

        // install them
        controls = {{
            onMouseEnter: highlight,
            onMouseLeave: reset,
        }}
    }}

    // size the shape
    const shrink = `scale(${{size / 1000}})`

    // paint me
    return (
        <div style={{badgeStyle}} {{...controls}} >
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width={{size}} height={{size}} >
                <g transform={{shrink}} style={{shapeStyle}} >
                    {{children}}
                </g>
            </svg>
        </div>
    )
}}


// publish
export default badge


// end of file
