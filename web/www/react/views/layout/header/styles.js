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
    // the style of the enclosing tag
    header: {
        position: "fixed",
        top: "0",
        left: "0",
        right: "0",
        zIndex: "9999",
        backgroundColor: wheel.chalk,
        borderBottom: `1px solid ${wheel.cement}`,

        display: "flex",
        flexDirection: "row",
        alignItems: "bottom",

        height: "2.0em",

        fontSize: "60%",
        margin: "0.0em 2.0em 0.0em 2.0em",
        padding: "1.0em 2.0em 1.0em 2.0em",

        color: wheel.steel,
    },

    // the logo
    logo: {
        height: "2.0em",
    },

    // navigation
    nav: {
        whiteSpace: "nowrap",
        paddingLeft: "2em",
    },

    navLink: {
        paddingLeft: "1.0em",
        paddingRight: "1.0em",
        lineHeight: "3.0em",
        textTransform: "lowercase",
        borderRight: `1px solid ${wheel.soapstone}`,
    },

    navLinkLast: {
        borderRight: "none",
        paddingRight: "0.0em",
    },
}

// end of file
