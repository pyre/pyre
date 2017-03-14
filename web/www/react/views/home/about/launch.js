// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'

// support
import Python from 'widgets/code/Python'

// the code snippet
const listing = `\
mga@cygnus:~/tmp> gauss.py
simple: volume = 3.141592653589793
mga@cygnus:~/tmp>
`

// dress up
const content = ({...props}) => (
    <Python {...props}>
        {listing}
    </Python>
)

// publish
export default content

// end of file
