// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ wheel, theme }} from '~/palette'
// get the base styles
import base from '~/views/styles'


// publish
export default {{
    // the container
    loading: {{
        // inherit
        ...base.panel,
    }},

    placeholder: {{
        position: "fixed",
        top: "50%",
        left: "50%",
        width: "100%",
        textAlign: "center",
        transform: "translate(-50%, -50%)",
    }},

    logo: {{
        // placement
        margin: "1.0em auto",
        width: "300px",
        height: "300px",

        // animation
        animationName: "fadeInOut",
        animationDuration: "3s",
        animationIterationCount: "infinite",
    }},

    shape: {{
        icon: {{
            fill: "none",
            strokeWidth: "5px",
        }},
    }},

    message: {{
        fontFamily: "inconsolata",
        fontSize: "120%",
        textAlign: "center",
    }},

}}


// end of file
