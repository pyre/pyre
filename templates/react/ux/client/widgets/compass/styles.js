// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ theme }} from '~/palette'


// publish
export default {{
    panel: {{
    }},

    north: {{
        // stroke
        stroke: "hsl(0deg,0%,20%)",
        // exclude the stroke from any transforms
        vectorEffect: "non-scaling-stroke",

        // fill
        fill: "none",
    }},

    east: {{
        // stroke
        stroke: "hsl(0deg,0%,20%)",
        // exclude the stroke from any transforms
        vectorEffect: "non-scaling-stroke",

        // fill
        fill: "none",
    }},

    needle: {{
        // stroke
        stroke: "hsl(0deg,50%,20%)",
        // exclude the stroke from any transforms
        vectorEffect: "non-scaling-stroke",

        // fill
        fill: "none",
    }},

    needletip: {{
        // stroke
        stroke: "none",
        // just in case we ever stroke this
        vectorEffect: "non-scaling-stroke",

        // fill
        fill: "hsl(0deg,50%,20%)",
        fillOpacity: "1",
    }},
}}


// end of file
