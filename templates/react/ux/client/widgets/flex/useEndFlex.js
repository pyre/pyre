// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
// context
import {{ Context }} from './context'


// support for terminating a flex
export default () => {{
    // flexing support
    const {{ setFlexingPanel, setDownstreamPanels, }} = React.useContext(Context)

    // when flexing ends
    const endFlex = (evt) => {{
        // stop this event from bubbling up
        evt.stopPropagation()
        // an quash any side effects
        evt.preventDefault()

        // reset the flexing panel
        setFlexingPanel(null)
        // and the pile of downstream panels
        setDownstreamPanels([])

        // all done
        return
    }}

    // build and return the context relevant to this panel
    return {{
        // end a panel resize sequence
        endFlex
    }}
}}


// end of file
