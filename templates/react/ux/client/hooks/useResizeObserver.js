// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
import {{ debounce, throttle }} from 'lodash'


// hook that listens to resize events
const useResizeObserver = ({{
    // a reference to the component whose size we care about; if {{null}}, a new one will be made
    ref = null,
    // an optional call back to invoke on size changes
    onResize = null,
    // {{mode}} is either "debounce" or "throttle"; see the {{lodash}} docs for {{options}}
    limiter = {{ mode: null, wait: 0, options: null }}
}} = {{}}) => {{
    // make a ref, in case the client didn't supply one
    const cref = ref ?? React.useRef(null)
    // attach a resize handler
    const handler = React.useRef(null)
    // storage for the element extent
    const [extent, setExtent] = React.useState({{height: undefined, width: undefined}})

    // figure out the event rate limiter strategy
    let limiterStrategy = null
    // if the client wants debouncing
    if (limiter.mode === "debounce") {{
        // debounce, from {{lodash}}
        limiterStrategy = debounce
    // if the client wants throttling
    }} else if (limiter.mode === "throttle") {{
        // throttle, from {{lodash}}
        limiterStrategy = throttle
    // otherwise
    }} else {{
        // no dress up
        limiterStrategy = (callback, ...args) => callback
    }}

    // layout effect? i think not
    React.useEffect(() => {{
        // make a notifier
        const notify = (extent) => {{
            // which updates our state with the element extent
            setExtent(prev => {{
                // if nothing has changed
                if (prev.width === extent.width && prev.height === extent.height) {{
                    // just return the previous state
                    return prev
                }}
                // notify the client
                onResize?.(extent)
                // and return the new state
                return extent
            }})
        }}

        // build the callback we will install with the resize observer
        const callback = targets => {{
            // go through the {{targets}}
            targets.forEach(target => {{
                // get the extent
                // N.B.: {{contentRect}} is considered the "legacy" interface and may be deprecated;
                //       consider {{contentBoxSize}} or {{borderBoxSize}}
                const extent = target?.contentRect ?? {{height: undefined, width: undefined}}
                // invoke the notifier
                notify(extent)
            }})
        }}

        // install the callback in the handler
        handler.current = limiterStrategy(callback, limiter.wait, limiter.options)
        // make a resize observer
        const observer = new window.ResizeObserver(handler.current)
        // and if there is anything to observe
        if (cref.current) {{
            // register it with the observer
            observer.observe(cref.current)
        }}

        // at clean up time
        return () => {{
            // disconnect
            observer.disconnect()
            // get the callback
            const callback = handler.current
            // if it exists and it has a cancel method, invoke it
            callback?.cancel?.()
            // all done
            return
        }}
    // dependencies: the client's handler
    }}, [ onResize ])

    // make the ref and the extent available
    return {{ ref: cref, extent }}
}}


// publish
export default useResizeObserver


// end of file
