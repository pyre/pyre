// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'


// setup the flex context
export const Context = React.createContext(
    // the default value that consumers see when accessing the context outside a provider
    {{
        // directional flags
        direction: "row",
        isRow: true,
        parity: 1,
        // direction dependent attributes
        mainPos: "left",
        crossPos: "top",
        mainExtent: "width",
        crossExtent: "height",
        minExtent: "minWidth",
        maxExtent: "maxWidth",
        // cursors
        cursor: "col-resize",
        // the transform that centers the separator handle in its parent space
        transform: "translate(-50%, 0%)",
        // panel management
        panels: null,
        addPanel: () => {{ throw new Error('no context provider') }},
        removePanel: () => {{ throw new Error('no context provider') }},
        // the flexing panel when a separator gets activated
        flexingPanel: null,
        setFlexingPanel: () => {{ throw new Error('no context provider') }},
        // the set of panels downstream from the flexing one
        downstreamPanels: null,
        setDownstreamPanels: () => {{ throw new Error('no context provider') }},
        // the location of the moving panel separator
        separatorLocation: null,
        setSeparatorLocation: () => {{ throw new Error('no context provider') }},
    }}
)


// the provider factory
export const Provider = ({{
    // the box orientation
    direction,
    // children
    children
}}) => {{
    // deduce the main axis
    const isRow = direction.startsWith("row")
    // and the order, which affects the correlation between mouse movement and extent update
    const parity = direction.endsWith("-reverse") ? -1 : 1

    // flex direction dependent attributes so we can access without checking every time
    const [mainPos, crossPos] = isRow ? ["left", "top"] : ["top", "left"]
    const [mainExtent, crossExtent] = isRow ? ["width", "height"] : ["height", "width"]
    const [minExtent, maxExtent] = isRow ? ["minWidth", "maxWidth"] : ["minHeight", "maxHeight"]
    // the cursor we show is also flex direction dependent
    const cursor = isRow ? "col-resize" : "row-resize"
    // and so is the transformation that places the draggable handle over the separator
    const transform = isRow ? "translate(-50%, 0)" : "translate(0, -50%)"

    // the set of known panels
    const [panels, setPanels] = React.useState(new Map())

    // the location of the mouse while a separator is being dragged
    const [separatorLocation, setSeparatorLocation] = React.useState(null)
    // the panel being flexed when a separator is activated
    const [flexingPanel, setFlexingPanel] = React.useState(null)
    // the panels that are candidates for absorbing the flexing
    const [downstreamPanels, setDownstreamPanels] = React.useState([])

    // higher level functions
    // registering a new panel
    const addPanel = ({{ panel, min, max, auto }}) => {{
        // update the panel pile
        setPanels(old => {{
            // clone the current pile
            const clone = new Map(old)
            // add the new panel info
            clone.set(panel, {{ min, max, auto }})
            // and return the new map
            return clone
        }})
        // all done
        return
    }}

    // removing a panel
    const removePanel = ({{ panel }}) => {{
        // update the panel pile
        setPanels(old => {{
            // clone the current pile
            const clone = new Map(old)
            // remove the panel that's going away
            clone.delete(panel)
            // and return the new pile
            return clone
        }})
        // all done
        return
    }}


    // build the current value of the context
    const context = {{
        // direction flags
        direction, isRow, parity,
        // direction dependent attribute names
        mainPos, crossPos, mainExtent, crossExtent, minExtent, maxExtent,
        // cursors
        cursor,
        // the transform that centers the separator handle within the rule
        transform,
        // panel management
        panels, addPanel, removePanel,
        // support for flexing
        flexingPanel, setFlexingPanel,
        separatorLocation, setSeparatorLocation,
        downstreamPanels, setDownstreamPanels,
    }}

    // provide for my children
    return (
        <Context.Provider value={{context}} >
            {{children}}
        </Context.Provider >

    )
}}


// end of file
