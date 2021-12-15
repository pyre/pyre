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
        panels,
        mainExtent, mainPos,
        hasFlexed, setHasFlexed,
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

        // get the panel refs
        const refs = Array.from(panels.keys())
        // collect placement and sizing information for all panels
        const extents = new Map(refs.map(ref => [ref, ref.current.getBoundingClientRect()]))

        // if this is the first time we are flexing
        if (!hasFlexed) {{
            // go through all the panels
            extents.forEach((extent, panelRef) => {{
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
                style[mainExtent] = `${{extent[mainExtent]}}px`
                // all done
                return
            }})
            // mark
            setHasFlexed(true)
        }}

        //  find the position of the flexing panel
        const pos = extents.get(panel)[mainPos]

        // the downstream panels are those panels
        const downstream = refs.filter(
            // whose position is greater than the flexing panel
            ref => extents.get(ref)[mainPos] > pos
        ).sort(
            // sorted in increasing order by their position
            (op1, op2) => extents.get(op1)[mainPos] - extents.get(op2)[mainPos]
        )

        // currently, disallow activity on the last separator
        if (downstream.length === 0) {{
            // so skip the state update if there are no downstream panels
            return
        }}

        // record the panel that is flexing
        setFlexingPanel(panel)
        // and the downstream ones
        setDownstreamPanels(downstream)
        // unpack the mouse coordinates and use them as the current separator location
        setSeparatorLocation({{ x: evt.clientX, y: evt.clientY }})

        // all done
        return
    }}

    // publish
    return {{ beginFlex }}
}}


// end of file
