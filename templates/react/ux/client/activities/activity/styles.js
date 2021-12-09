// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ theme }} from '~/palette'


// publish
export default {{
    // for the badge
    badge: {{
    }},

    // for the shape
    shape: {{
        // dim it a bit
        fillOpacity: 0.5,
        strokeOpacity: 0.5,
    }},

    // state dependent overrides
    // when this is the current activity
    engaged: {{
        // for the badge
        badge: {{
            borderLeft: "2px solid white",
        }},
        // for the shape
        shape: {{
            // full intensity
            fillOpacity: 1.0,
            strokeOpacity: 1.0,
        }},
    }},

    // when exploring whether this activity is available; e.g. when the cursor hovers over its badge
    available: {{
        // for the badge
        badge: {{
        }},
        // for the shape
        shape: {{
            // full intensity
            fillOpacity: 1.0,
            strokeOpacity: 1.0,
        }},
    }},

    // when the activity is not available
    disabled: {{
        // for the badge
        badge: {{
        }},
        // for the shape
        shape: {{
            // dim it a lot
            fillOpacity: 0.2,
            strokeOpacity: 0.2,
        }},
    }},
}}


// end of file
