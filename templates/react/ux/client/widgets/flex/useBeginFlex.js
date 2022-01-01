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
        setSeparatorLocation, setFlexingPanel, setDownstreamPanels,
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

        // disable flexbox for all panels while we resize them
        // go through all the panels
        extents.forEach((extent, panelRef) => {{
            // get the style of the associated element
            const style = panelRef.current.style
            // turn flex off
            style.flex = "0 0 auto"
            // and make sure the panel style reflects the current actual extent
            style[mainExtent] = `${{extent[mainExtent]}}px`
            // all done
            return
        }})


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
