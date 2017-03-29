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
        flexDirection: "row",
    },

    body: {
        textAlign: "justify",
        margin: "0.5em 0.0em 0.5em 0.0em",
        padding: "0.0em 0.0em 0.0em 0.0em",
    },

    section: {

        container: {
            display: "flex",
            flexDirection: "column",

            fontSize: "120%",
            //margin: "1em 1em 1em 1em",
        },

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
    },

    toc: {
        table: {
            flexGrow: 0,
            margin: "1.0em 0.0em",
        },

        title: {
            fontSize: "120%",
            lineHeight: "150%",
            textTransform: "uppercase",
            color: semantic.section.title.text,
        },

        item: {
            lineHeight: "175%",
        },

        contents: {
            marginLeft: "2em",
        }
    },
}

// publish
export default document



// end of file
