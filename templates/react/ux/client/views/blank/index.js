// -*- web -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
import React from 'react'
// locals
// hooks
import {{ useResizeObserver }} from '~/hooks'
// styles
import styles from './styles'


// the area
const blank = () => {{
    // get my extent
    const {{ ref, extent }} = useResizeObserver()

    // render
    return (
        <section ref={{ref}} style={{styles.extent}}>
            {{extent.height}}x{{extent.width}}
        </section>
    )
}}


// publish
export default blank


// end of file
