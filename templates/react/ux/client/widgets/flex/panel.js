// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'

// project
// hooks
import {{ useResizeObserver }} from '~/hooks'

// locals
// hooks
import useBeginFlex from './useBeginFlex'
import useRegisterPanel from './useRegisterPanel'
import useDirectionalAttributes from './useDirectionalAttributes'
// my separator
import Separator from './separator'
// styles
import styles from './styles'


// a container for client children
export const Panel = ({{
    min = 0, max = Infinity, auto = false, debug = false,
    style, children, ...rest
}}) => {{
    // register this panel and make a {{ref}} for it
    const panel = useRegisterPanel({{ min, max, auto }})
    // get support for initiating flexing
    const flexProps = useBeginFlex({{ panel }})
    // get the direction dependent extent names
    const {{ minExtent, maxExtent }} = useDirectionalAttributes()

    // storage for the size dependent styling
    let sizeStyle = {{}}
    // if i have a minimum size
    if (min > 0) {{
        // attach it to my style object; make the units explicit so there is no confusion
        sizeStyle[minExtent] = `${{min}}px`
    }}
    // if i have a maximum size
    if (max < Infinity) {{
        // attach it to my style object; make the units explicit so there is no confusion
        sizeStyle[maxExtent] = `${{max}}px`
    }}

    // mix my paint
    const panelStyle = {{ ...styles.panel, ...sizeStyle, ...style?.panel }}

    // during normal execution, my content is my {{children}}
    let content = children
    // however, in debugging mode
    if (debug) {{
        // get my extent
        const {{ extent }} = useResizeObserver({{ ref: panel }})
        // and render it as my content
        content = <span style={{styles.extent}}>debug: {{extent.width}}x{{extent.height}}</span>
    }}

    // paint me
    return (
        <>
            <div ref={{panel}} style={{panelStyle}} {{...rest}} >
                {{content}}
            </div>
            <Separator {{...flexProps}} style={{style.separator}} />
        </>
    )
}}


// end of file
