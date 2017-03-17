// -*- web -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
import { Link } from 'react-router-dom'

// support
import { Pyre, Subsection, Paragraph, TableOfContents, Content } from 'widgets/doc'
// locals
import styles from './styles'

// declaration
const Syllabus = () => (
    <Subsection title="Syllabus">
        <Paragraph>
            The material here is derived from a semester long course on using <Pyre/> to
            write scientific applications. The lecture notes are written
            using <code>beamer</code> and are bundled with the source code.
        </Paragraph>

        <TableOfContents>
            <Content title="from the end user's point of view">
                <Content>
                    <Link to="/docs/course/overview">
                        overview of <Pyre/>
                    </Link>
                </Content>
                <Content title="capturing user choices"/>
                <Content title="writing components"/>
            </Content>
            <Content title="for application developers">
                <Content title="assembling applications"/>
                <Content title="command line user interfaces"/>
                <Content title="writing extensions in C and C++"/>
                <Content title="support: journal, memory, arrays, MPI, CUDA, databases"/>
            </Content>
            <Content title="framework internals">
                <Content title="data structures, evaluation networks, traits and their schemata"/>
                <Content title="component configuration"/>
                <Content title="runtime environment discovery"/>
                <Content title="advanced techniques: user interfaces,
                                asynchronous and concurrent execution" />
            </Content>
        </TableOfContents>
    </Subsection>
)

//   publish
export default Syllabus

// end of file
