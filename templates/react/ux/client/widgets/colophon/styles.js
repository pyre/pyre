// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ wheel, theme }} from '~/palette'


// publish
export default {{
    // styling the overall container
    box: {{
    }},

    // the copyright note
    copyright: {{
        fontFamily: "\"helvetica\", \"arial\", \"sans-serif\"",
        color: theme.colophon.copyright,
        fontWeight: "normal",
    }},

    // the author
    author: {{
        color: theme.colophon.author,
    }},
}}


// end of file
