// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import {{ useEffect }} from 'react'


// register a {{listener}} with {{client}} for the given event {{name}} that gets updated
// whenever {{triggers}} are modified
export default ({{
    name = throwError(), listener = throwError(), client = null, triggers = []
}}) => {{
    // create an effect
    useEffect(() => {{
        // figure out the effect target
        const target = client?.current || window
        // add {{listener}} as an event listener
        target.addEventListener(name, listener)
        // make a controller; not sure whether this is required, useful, harmful...
        const controller = new AbortController()
        // and register a clean up
        return () => {{
            // that removes the listener
            target.removeEventListener(name, listener)
            // and aborts any pending requests
            controller.abort()
        }}
    }},
        // register the refresh {{triggers}}
        triggers
    )
    // all done
    return
}}


// end of file
