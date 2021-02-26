// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import base from './styles'


// the flame
const flame = `
M 100 0
C 200 75 -125 160 60 300
C 20 210 90 170 95 170
C 80 260 130 225 135 285
C 160 260 160 250 155 240
C 180 260 175 270 170 300
C 205 270 240 210 195 135
C 195 165 190 180 160 200
C 175 180 220 55 100 0
Z`


// the bar at the bottom of every page
const widget = ({{style, ...xforms}}) => (
    // the container
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" style={{{{...base.box, ...style.box}}}}>
        {{/* the shape */}}
        <g {{...base.shape}} {{...style.shape}} {{...xforms}}>
            <path d={{flame}}/>
        </g>
    </svg>
)


// publish
export default widget


// end of file
