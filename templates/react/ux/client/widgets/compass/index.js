// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
import React from 'react'
// locals
import base from './styles'


// a scale and orientation indicator
const compass = ({{style, ...xforms}}) => (
    <g {{...base.panel}} {{...style}} {{...xforms}}>
        <line x1="-1" y1="0" x2="1" y2="0"
              {{...base.east}} {{...style?.east}} />

        <line x1="0" y1="-1" x2="0" y2="1"
              {{...base.north}} {{...style?.north}} />

        <circle cx="0" cy="0" r=".1"
              {{...base.needle}} {{...style?.needle}} />

        <path d="M -0.14142 0.14142
                 C 0 .25 0 .25 0.14142 0.14142
                 L 0 .3
                 Z"
              {{...base.needletip}} {{...style?.needletip}} />

        <path d="M 0.14142 -0.14142
                 C .3 0 .3 0 0.14142 0.14142
                 L .3 0
                 Z"
              {{...base.needletip}} {{...style?.needletip}} />
    </g>
)


// publish
export default compass


// end of file
