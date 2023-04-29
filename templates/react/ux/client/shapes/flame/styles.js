// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ theme }} from '~/palette'

// the base style
import style from '~/shapes/styles'


// the shape color
const ink = "hsl(28deg, 90%, 35%)"
const paint = "hsl(28deg, 90%, 55%)"

// publish
export default {{
    // the main shape
    icon: {{
        // inherit
        ...style.icon,
        // stroke
        stroke: ink,
        // fill
        fill: paint,
    }},

    // decorative touches
    decoration: {{
        // inherit
        ...style.decoration,
    }},
}}


// end of file
