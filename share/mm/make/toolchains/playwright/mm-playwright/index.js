// -*- web -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
const childProcess = require("child_process")
const fs = require("fs")
const path = require("path")


// the launch options a browser {engine} needs on this platform, for a suite whose scratch area is
// {scratch}; a suite spreads them into the {use} block of its configuration, e.g.
//     use: { ...devices["Desktop Firefox"], launchOptions: launchOptions({ engine, scratch }) }
const launchOptions = ({ engine, scratch }) => {
    // macOS keeps the data folder of an installed application, e.g. the one of an installed
    // Firefox in {~/Library/Application Support/Firefox}, out of reach of other applications; the
    // Firefox of the toolchain is another application with the same name, so it is turned away
    // from that folder and gives up before it starts, saying it cannot find its profile
    if (engine === "firefox" && process.platform === "darwin") {
        // so it gets a home of its own in the scratch area, where it finds nothing it may not touch
        const home = path.join(scratch, "firefox-home")
        // made here, since the browser expects it to be there
        fs.mkdirSync(home, { recursive: true })
        // and handed to the browser alone, through {CFFIXED_USER_HOME}, which macOS consults
        // before the real home; the rest of the suite, e.g. the servers it tests, keeps the real one
        return { env: { ...process.env, CFFIXED_USER_HOME: home } }
    }
    // every other engine and platform needs nothing
    return {}
}


// undo what {launchOptions} set up in the {scratch} area, so a suite can remove it; call it before
// removing the scratch area
const release = ({ scratch }) => {
    // the home the firefox of the toolchain gets on macOS
    const home = path.join(scratch, "firefox-home")
    // on other platforms, or when there is none
    if (process.platform !== "darwin" || !fs.existsSync(home)) {
        // there is nothing to undo
        return
    }
    // macOS lays out {Library}, {Documents}, and {Downloads} in that home the way it does in a real
    // one, with an access control entry that forbids deleting them; clear every such entry, with
    // the {chmod} of the system, since others do not know about them
    childProcess.execFileSync("/bin/chmod", ["-RN", home])
    // all done
    return
}


// publish
module.exports = { launchOptions, release }


// end of file
