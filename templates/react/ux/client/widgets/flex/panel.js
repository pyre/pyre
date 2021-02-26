// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'

// locals
// hooks
import {{ useResizeObserver }} from '~/hooks'
// hooks
import useBeginFlex from './useBeginFlex'
import useRegisterPanel from './useRegisterPanel'
import useDirectionalAttributes from './useDirectionalAttributes'
// my separator
import Separator from './separator'
// styles
import styles from './styles'


// a container for client children
const panel = ({{ min = 0, max = Infinity, style, children, debug }}) => {{
    // register this panel and make a {{ref}} for it
    const ref = useRegisterPanel({{ min, max }})
    // get support for initiating flexing
    const flexProps = useBeginFlex({{ panel: ref }})
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
        const {{ extent }} = useResizeObserver({{ ref }})
        // and render it as my content
        content = <span>{{extent.width}}x{{extent.height}}</span>
    }}

    // paint me
    return (
        <>
            <div ref={{ref}} style={{panelStyle}} >
                {{content}}
            </div>
            <Separator {{...flexProps}} style={{style.separator}} />
        </>
    )
}}


// publish
export default panel


// end of file
