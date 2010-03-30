<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2009  all rights reserved
!
-->

<config 
   xmlns="http://pyre.caltech.edu/releases/1.0/schema/config.html"
   xmlns:pyre="http://pyre.caltech.edu/releases/1.0/schema/config.html"
   xsi:schemaLocation="http://pyre.caltech.edu/releases/1.0/schema/config.html
                       http://pyre.caltech.edu/releases/1.0/schema/config.xsd">

  <inventory name="pyre">
    <!-- some global settings -->
    <bind property="home">pyre.home()</bind>
    <bind property="prefix">pyre.prefix()</bind>

    <!-- and some per user settings -->
    <inventory name="user">
      <bind property="name">michael a.g. aïvázis</bind>
      <bind property="email">aivazis@caltech.edu</bind>
    </inventory>

  </inventory>

  <bind property="pyre.user.affiliation">california institute of technology</bind>

</config>


<!-- end of file -->
