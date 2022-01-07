// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
// context
import {{ Context }} from './context'


// flex support
export default () => {{
    // grab the state mutator
    const {{
        // directional
        isRow, parity, mainExtent,
        // the registered panels
        panels,
        // flexing support
        flexingPanel,
        downstreamPanels,
        separatorLocation, setSeparatorLocation,
    }} = React.useContext(Context)

    // while we are flexing
    const doFlex = (evt) => {{
        // stop this event from bubbling up
        evt.stopPropagation()
        // an quash any side effects
        evt.preventDefault()

        // if no panel is flexing
        if (flexingPanel == null) {{
            // nothing to do
            return
        }}

        // unpack the cursor position
        const {{ clientX: x, clientY: y }} = evt

        // unpack the location of the last update
        const {{ x: oldX, y: oldY }} = separatorLocation
        // compute the proposed size change
        const delta = parity * (isRow ? (x - oldX) : (y - oldY))
        // if we are just sliding along the cross axis
        if (Math.abs(delta) < 1) {{
            // don't go any further
            return
        }}

        // cap the proposed {{delta}} to what the flexing panel can accommodate
        const allowed = clip(flexingPanel, delta)
        // if no change is permitted
        if (allowed == 0) {{
            // nothing further to do
            return
        }}

        // otherwise, let's batch the size changes into a transaction that we can abort
        // if we can't find a resizing solution
        const updates = new Array()
        // the first candidate is the flexing panel itself
        updates.push([flexingPanel, allowed])

        // keep track of how much change must be accommodated
        let remaining = - allowed
        // go through the panels downstream from the flexing one
        for (const panel of downstreamPanels) {{
            // compute how much this one can absorb
            const absorbed = clip(panel, remaining)
            // if it can participate
            if (absorbed != 0) {{
                // add it to the resizing transaction
                updates.push([panel, absorbed])
            }}
            // update the remaining size change and move on to the next downstream panel
            remaining -= absorbed
        }}

        // if we failed to absorb everything
        if (Math.trunc(remaining) != 0) {{
            // punt; the proposed size change cannot be accommodated
            return
        }}
        // otherwise, update the sizes of every panel that flexes
        resize(updates)

        // record the new reference location
        setSeparatorLocation({{ x, y }})

        // all done
        return
    }}

    // clip the proposed extent change to the user supplied range
    const clip = (panel, delta) => {{
        // get the panel node
        const node = panel.current
        // compute its extents
        const extent = node.getBoundingClientRect()[mainExtent]
        // unpack the size hints that were registered for this panel
        const {{ min, max }} = panels.get(panel)
        // in order to do the clipping
        const allowed = Math.trunc(
            // first figure out which way we plan to push the limits
            (delta > 0)
                // on stretch: no more than {{maxSize}} permits
                ? Math.min(delta, max - extent)
                // on shrink: no less that {{minSize}} permits
                : Math.max(delta, min - extent))
        // all done
        return allowed
    }}

    // update the extents of the panels in given a batch of size changes
    const resize = (updates) => {{
        // go through the updates
        for (const [panel, delta] of updates) {{
            // get the node
            const node = panel.current
            // compute the new extent
            const extent = node.getBoundingClientRect()[mainExtent] + delta
            // and use it to style the node
            node.style[mainExtent] = `${{extent}}px`
        }}
        // all done
        return
    }}

    // build and return the context relevant to this panel
    return {{
        // provide access to the current flexing panel
        flexingPanel,
        // the location of the separator
        separatorLocation,
        // compute a resize solution
        doFlex,
    }}
}}


// end of file
