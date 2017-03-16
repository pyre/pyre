// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
import { Link } from 'react-router-dom'

// locals
import document from './styles'

// render
const Pyre = () => (
    <Link to="/">
        <span style={document.pyre}>pyre</span>
    </Link>
)

// publish
export default Pyre

// end of file
