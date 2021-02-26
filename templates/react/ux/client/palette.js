// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// a color wheel
const wheel = {{
    // greys; the names are borrowed from {{omni graffle}}
    gray: {{
        obsidian: "#000",
        basalt: "#333333",
        gabro: "#424242",
        steel: "#666",
        shale: "#686868",
        flint: "#8a8a8a",
        granite: "#9a9a9a",
        aluminum: "#a5a5a5",
        concrete: "#b8b8b8",
        soapstone: "#d6d6d6",
        cement: "#eee",
        marble: "#f1f1f1",
        flour: "#fafafa",
        chalk: "#ffffff",
    }},

    // pyre colors
    pyre: {{
        blue: "hsl(203deg, 77%, 60%)",
        green: "hsl(63deg, 40%, 50%)",
        orange: "hsl(31deg, 80%, 58%)",
    }},

    // journal colors
    journal: {{
        error: "hsl(0deg, 90%, 50%)",
    }}
}}


// my dark theme
const dark = {{
    // the page
    page: {{
        background: "hsl(0deg, 0%, 5%)",
        appversion: "hsl(0deg, 0%, 25%)",
    }},

    // the header
    banner: {{
        // overall styling
        background: "hsl(0deg, 0%, 7%)",
        separator: "hsl(0deg, 0%, 15%)",
        // contents
        name: "hsl(28deg, 90%, 55%)",
        // menu
        nav: {{
            link: "hsl(28deg, 20%, 50%)",
            current: "hsl(28deg, 20%, 70%)",
            inactive: "hsl(28deg, 20%, 20%)",
            separator: "hsl(0deg, 0%, 35%)",
        }},
    }},

    statusbar: {{
        // overall styling
        background: "hsl(0deg, 0%, 31%)",
        separator: "hsl(0deg, 0%, 15%)",
    }},

    // app metadata
    colophon: {{
        // contents
        copyright: "hsl(0deg, 0%, 40%)",
        author: "hsl(0deg, 0%, 40%)",
    }},

    // widgets
    widgets: {{
        background: "hsl(0deg, 0%, 7%)",
    }},

    // journal colors
    journal: wheel.journal,
}}


// my default theme
const theme = dark


// publish
export {{ wheel, dark, theme }}


// end of file
