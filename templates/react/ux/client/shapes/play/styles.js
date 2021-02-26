// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ theme }} from '~/palette'

// the base style
import style from '~/shapes/styles'


// the shape color
const ink = "hsl(0deg, 0%, 90%)"
const paint = "hsl(0deg, 0%, 70%)"

// publish
export default {{
    // the main shape
    icon: {{
        // inherit
        ...style.icon,
        // stroke
        stroke: ink,
        strokeWidth: 1,
        // fill
        fill: "none",
    }},

    // decorative touches
    decoration: {{
        // inherit
        ...style.decoration,
        // stroke
        stroke: ink,
        // fill
        fill: paint,
    }},
}}


// end of file
