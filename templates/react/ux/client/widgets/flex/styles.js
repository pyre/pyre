// -*- web -*-
//
// {project.authors}
// (c) 1998-2020 all rights reserved


// get colors
import {{ wheel, theme }} from '~/palette'
// get the base styles
import base from '~/views/styles'


// publish
export default {{
    // the overall box
    box: {{
        position: "relative",
        overflow: "clip",
        display: "flex",
        width: "100%",
        height: "100%",
    }},

    // the individual panels
    panel: {{
        // for me
        flex: "1 1 100%",
        // for my children
        overflow: "hidden",
        display: "flex",
    }},

    // the inter-panel separator
    separator: {{
        // the line
        rule: {{
            flex: "0 0 auto",
            overflow: "visible",
            backgroundColor: "hsl(0deg, 0%, 15%, 0.5)",
            zIndex: 1,
        }},

        // the handle
        handle: {{
        }},

        // state dependent styling
        colors: {{
            hidden: "hsl(0deg, 0%, 25%, 0)",
            visible: "hsl(28deg, 30%, 25%, 0.5)",
        }},
    }},

    // in debug mode, we just show the size of the panel
    extent: {{
        // fonts
        fontFamily: "inconsolata",
        fontSize: "60%",

        // take up all available space
        width: "100%",
        height: "100%",

        // make it stand out
        color: theme.banner.name,
        backgroundColor: "hsl(0, 20%, 7%)",
    }},
}}


// end of file
