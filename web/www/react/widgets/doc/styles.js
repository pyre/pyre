// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// colors
import { wheel, semantic } from 'palette'

// define
const document = {

    pyre: {
        color: semantic.pyre,
    },

    page: {
        display: "flex",
        flexDirection: "column",

        fontSize: "120%",
        //margin: "1em 1em 1em 1em",
    },

    body: {
        textAlign: "justify",
        margin: "0.5em 0.0em 0.5em 0.0em",
        padding: "0.0em 0.0em 0.0em 0.0em",
    },

    section: {

        bar: {
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            margin: "1.0em 0.0em 1.0em 0.0em",
            padding: "0.25em 1.5em 0.25em 1.5em",
            backgroundColor: semantic.section.title.banner,
        },

        title: {
            fontWeight: "normal",
            fontSize: "150%",
            lineHeight: "200%",

            textTransform: "uppercase",
            color: semantic.section.title.text,
        },

        logo: {
            height: "1.25em",
            marginLeft: "auto",
        },
    },

    subsection: {

        bar: {
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            margin: "1.0em 0.0em 1.0em 0.0em",
            padding: "0.25em 0em 0.25em 0em",
        },

        title: {
            fontWeight: "normal",
            fontSize: "120%",
            lineHeight: "150%",

            textTransform: "uppercase",
            color: semantic.section.title.text,
        },
    }
}

// publish
export default document



// end of file
