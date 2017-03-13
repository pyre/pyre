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
            <Link to="#about" style={styles.navLink}>
                about
            </Link>
            <Link to="#download" style={styles.navLink}>
                get
            </Link>
            <Link to="#documentation" style={styles.navLink}>
                docs
            </Link>
            <Link to="#contact" style={{...styles.navLink, ...styles.navLinkLast}}>
                contact
            </Link>
        </nav>
    </header>
)

// export
export default header

// end of file
