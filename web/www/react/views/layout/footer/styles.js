// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// get the colors
import { wheel, semantic } from 'palette'

// publish
export default {
    //
    footer : {
        position: "fixed",
        bottom: "0",
        left: "0",
        right: "0",
        zIndex: "9999",

        fontSize: "50%",
        margin: "0.0em 2.0em 0.0em 2.0em",
        padding: "1.0em 2.0em 1.0em 2.0em",
        textAlign: "right",

        color: wheel.soapstone,
        backgroundColor: wheel.chalk,
        borderTop: `1px solid ${wheel.soapstone}`,

    },

    copyright : {
        fontWeight: "normal",
        fontSize: "100%",
    },
}

// end of file
