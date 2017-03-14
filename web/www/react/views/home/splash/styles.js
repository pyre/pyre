// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// colors
import { wheel, semantic } from "palette"

// publish
export default {

    // the top-level container
    section: {
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-evenly",
        alignItems: "center",
        margin: "3.0em 2.0em 1.0em 2.0em",
        padding: "1.0em 0.0em 1.0em 0.0em",
    },

    leader: {
        fontSize: "120%",
        fontWeight: "normal",
        lineHeight: "150%",
        whiteSpace: "nowrap",
        textTransform: "uppercase",
        color: wheel.aluminum,
    },

    title: {
        fontSize: "200%",
        fontWeight: "normal",
        lineHeight: "300%",
        whiteSpace: "nowrap",
        textTransform: "uppercase",
        color: semantic.title,
    },

    abstract: {
        fontFamily: "georgia",
        fontStyle: "italic",
        fontSize: "100%",
        lineHeight: "150%",
        margin: "0.5em auto 0.5em auto",
        textAlign: "center",
        width: "30em",
        color: wheel.aluminum,
    },

    navigation: {
        display: "flex",
        flexDirection: "row",
        margin: "2.0em 0.0em 1.0em 0.0em",
        alignItems: "center",
        justifyContent: "space-evenly",
    },

    button: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        height: "3em",
        width: "10em",
        margin: "1.0em 2.0em 1.0em 2.0em",
        border: `solid 1px ${semantic.button.border}`,
        borderRadius: "0.5em",
    },

    label: {
        textTransform: "uppercase",
        margin: "auto 0.0em auto 0.0em",
        color: semantic.button.label,
    },
}

// end of file
