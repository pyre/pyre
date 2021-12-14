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
        panels,
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
            // collect the current sizes
            const extents = refs.map(
                panelRef => Math.round(panelRef.current.getBoundingClientRect()[mainExtent])
            )

            // go through all the panels
            refs.forEach((panelRef, idx) => {{
                // grab the extent of the current panel
                const extent = extents[idx]
                // check whether the user has marked this panel as able to absorb viewport changes
                const {{ auto }} = panels.get(panelRef)
                // deduce the correct flex: every panel is now frozen to its styled extent,
                // except the ones marked auto
                const flx = auto ? "1 1 auto" : "0 0 auto"

                // get the style of the associated node
                const style = panelRef.current.style
                // apply the flex
                style.flex = flx
                // transfer its current extent to the its style
                style[mainExtent] = `${{extent}}px`
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
