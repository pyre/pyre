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
const Section = ({id, title, logo, children, style}) => (
    <section id={id} style={{...document.section.container, ...style}}>
        <Title logo={logo} style={document.section}>
            {title}
        </Title>
        {children}
    </section>
)

// defaults
Section.defaultProps = {
    id: "unused",
    logo: true,
    title: "please specify the section title",
}

// publish
export default Section

// end of file
