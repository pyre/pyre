// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
// context
import {{ Context }} from './context'


// support for initiating
export default ({{ panel }}) => {{
    // grab the state mutator
    const {{
        mainExtent,
        panels, addPanel,
        isManaged, setIsManaged,
        setSeparatorLocation,
        setFlexingPanel,
        setDownstreamPanels,
    }} = React.useContext(Context)

    // when a panel starts flexing
    const beginFlex = (evt) => {{
        // stop this event from bubbling up
        evt.stopPropagation()
        // quash any side effects
        evt.preventDefault()

        // unpack the cursor location
        const location = {{ x: evt.clientX, y: evt.clientY }}

        // get the panel refs
        const refs = Array.from(panels.keys())
        // find the index of the active panel
        const idx = refs.indexOf(panel)
        // use it to extract all the downstream panels
        const downstream = refs.slice(idx + 1)

        // currently, disallow activity on the last separator; so skip the state update
        // if there are no downstream panels
        if (downstream !== []) {{
            // record the panel that is flexing
            setFlexingPanel(panel)
            // and the downstream ones
            setDownstreamPanels(downstream)
            // save the current mouse coordinates
            setSeparatorLocation(location)
        }}

        // if this is the first time we are flexing
        if (!isManaged) {{
            // go through all the panels
            refs.forEach((panelRef, idx) => {{
                // get the associated container
                const node = panelRef.current
                // measure it
                const extent = Math.round(node.getBoundingClientRect()[mainExtent])
                // transfer its current extent to the its style
                node.style[mainExtent] = `${{extent}}px`
                // deduce the correct flex: every panel is now frozen to its styled extent,
                // except the last one that becomes responsible for absorbing viewport size changes
                const flx = (idx == refs.length - 1) ? "1 1 0" : "0 0 auto"
                // and apply it
                node.style.flex = flx
                // all done
                return
            }})
            // mark
            setIsManaged(true)
        }}

        // all done
        return
    }}

    // publish
    return {{ beginFlex }}
}}


// end of file
