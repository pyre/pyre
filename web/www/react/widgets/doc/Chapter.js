// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
// locals
import document from './styles'
import Title from './SectionTitle'

// render
const Chapter = ({id, title, logo, children, style}) => (
    <section id={id} style={{...document.chapter.container, ...style}}>
        <Title logo={logo} style={document.chapter}>
            {title}
        </Title>
        {children}
    </section>
)

// defaults
Chapter.defaultProps = {
    id: "unused",
    logo: true,
    title: "please specify the chapter title",
}

// publish
export default Chapter

// end of file
