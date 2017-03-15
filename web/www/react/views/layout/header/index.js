// -*- jsx -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// externals
import React from 'react'
import { Link } from 'react-router-dom'

// locals
import styles from './styles'

// declare
const header = () => (
    <header style={styles.header}>
        <img style={styles.logo} src="graphics/logo.png" />
        <nav style={styles.nav}>
            <a href="#about" style={styles.navLink}>
                about
            </a>
            <a href="#install" style={styles.navLink}>
                get
            </a>
            <a href="#documentation" style={styles.navLink}>
                docs
            </a>
            <a href="#contact" style={{...styles.navLink, ...styles.navLinkLast}}>
                contact
            </a>
        </nav>
    </header>
)

// export
export default header

// end of file
