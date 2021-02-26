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
        // the flexing panel when a separator gets activated
        flexingPanel: null,
        setFlexingPanel: () => {{ throw new Error('no context provider') }},
        // the set of panels downstream from the flexing one
        downstreamPanels: null,
        setDownstreamPanels: () => {{ throw new Error('no context provider') }},
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

    // direction dependent styling attributes
    const [mainExtent, crossExtent] = isRow ? ["width", "height"] : ["height", "width"]
    const [minExtent, maxExtent] = isRow ? ["minWidth", "maxWidth"] : ["minHeight", "maxHeight"]
    const cursor = isRow ? "col-resize" : "row-resize"
    const transform = isRow ? "translate(-50%, 0)" : "translate(0, -50%)"

    // the registered panels
    const [panels, setPanels] = React.useState(new Map())

    // indicator of whether we have taken control of the panel extents
    const [isManaged, setIsManaged] = React.useState(false)
    // the location of the mouse as a separator is being dragged
    const [separatorLocation, setSeparatorLocation] = React.useState(null)
    // the panel being flexed when a separator is activated
    const [flexingPanel, setFlexingPanel] = React.useState(null)
    // the panels that are candidates for absorbing the flexing
    const [downstreamPanels, setDownstreamPanels] = React.useState([])

    // higher level functions
    // registering a new panel
    const addPanel = ({{ ref, min, max }}) => {{
        // update the panel pile
        setPanels(old => new Map([...old, [ref, [min, max]]]))
        // all done
        return
    }}

    // build the current value of the context
    const context = {{
        // direction flags
        direction, isRow, parity,
        // direction dependent styling attribute names
        mainExtent, crossExtent, minExtent, maxExtent,
        // cursors
        cursor,
        // the transform that centers the separator handle within the rule
        transform,
        // panel management
        panels, addPanel,
        // managed panels have extents under our control after the first resize
        isManaged, setIsManaged,
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
