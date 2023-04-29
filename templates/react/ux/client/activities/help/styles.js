// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ theme }} from '~/palette'


// publish
export default {{
    // the container
    badge: {{
    }},

    // the shape
    shape: {{
    }},

    // state dependent overrides
    // when this is the current activity
    engaged: {{
        // for the badge
        badge: {{
        }},
        // for the shape
        shape: {{
        }},
    }},

    // when exploring whether this activity is available
    // e.g. when the cursor hovers over its badge
    available: {{
        // for the badge
        badge: {{
        }},
        // for the shape
        shape: {{
        }},
    }},

    // when the activity is not available
    disabled: {{
        // for the badge
        badge: {{
        }},
        // for the shape
        shape: {{
        }},
    }},
}}


// end of file
