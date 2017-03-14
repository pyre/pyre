// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// theming support
import { theme } from 'palette'

// publish
export default {

    code: {
        margin: "0.0em 0.0em 0.0em 0.0em",
        padding: "0.0em 0.0em 0.0em 0.0em",
        display: "flex",
        flexDirection: "row",
    },

    lineNumberContainer: {
        display: "flex",
        flexDirection: "column",
        flexGrow: 0,
        paddingRight: "1.0em",
        color: theme.lineNumber,
    },

    lineNumber: {
        textAlign: "right",
    },
}

// end of file
