// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
import {{ Link, useLocation }} from 'react-router-dom'

// locals
// widgets
import {{ Badge }} from '~/widgets'
// styles
import styles from './styles'


// the base activity rendering mechanics
// an activity is a {{Link}} that presents a {{shape}} inside a {{Badge}}
// {{shape}} is typically an SVG fragment

// activities can be {{ "engaged", "available", "disabled" }}
// currently, there is no use case for a disabled activity, so the logic may need to change

const activity = ({{ size, url, children, barStyle, style }}) => {{
    // get the current location
    const location = useLocation().pathname
    // check whether this is the current activity
    const state = location.startsWith(url) ? "engaged" : "available"

    // mix my paint
    const activityStyle = {{
        // for the badge
        badge: {{
            ...styles.badge,
            ...barStyle?.badge,
            ...style?.badge,
        }},
        // for the shape
        shape: {{
            ...styles.shape,
            ...barStyle?.shape,
            ...style?.shape,
        }},

        // for disabled activities
        disabled: {{
            // for the badge
            badge: {{
                ...styles.disabled.badge,
                ...barStyle?.disabled?.badge,
                ...style?.disabled?.badge,
            }},
            // for the shape
            shape: {{
                ...styles.disabled.shape,
                ...barStyle?.disabled?.shape,
                ...style?.disabled?.shape,
            }},
        }},
        // for engaged activities
        engaged: {{
            // for the badge
            badge: {{
                ...styles.engaged.badge,
                 ...barStyle?.engaged?.badge,
                 ...style?.engaged?.badge,
                 }},
            // for the shape
            shape: {{
                ...styles.engaged.shape,
                ...barStyle?.engaged?.shape,
                ...style?.engaged?.shape,
            }},
        }},
        // when answering the question whether an activity is available
        available: {{
            // for the badge
            badge: {{
                ...styles.available.badge,
                ...barStyle?.available?.badge,
                ...style?.available?.badge,
            }},
            // for the shape
            shape: {{
                ...styles.available.shape,
                ...barStyle?.available?.shape,
                ...style?.available?.shape,
            }},
        }},
    }}

    // paint me
    return (
        <Link to={{url}} >
            <Badge name={{url}} size={{size}} state={{state}} style={{activityStyle}} >
                {{children}}
            </Badge >
        </Link >
    )
}}


// publish
export default activity


// end of file
