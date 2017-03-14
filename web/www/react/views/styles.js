// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

import { wheel, semantic } from 'palette'

// publish
export default {

    sections: {
        section: {
            fontSize: "120%",
            display: "flex",
            flexDirection: "column",
            margin: "1em 1em 1em 1em",
            borderTop: `1px solid ${wheel.soapstone}`,
        },

        title: {
            fontSize: "150%",
            fontWeight: "normal",
            fontHeight: "200%",
            textTransform: "uppercase",
            margin: "1.0em 0.0em 1.0em 0.0em",
            padding: "0.25em 1.5em 0.25em 1.5em",
            color: semantic.section.title.text,
            backgroundColor: semantic.section.title.banner,
        },

        body: {
            margin: "0.5em 0.0em 0.5em 0.0em",
            padding: "0.0em 2.0em 0.0em 2.0em",
        },
    },
}
