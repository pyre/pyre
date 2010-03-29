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
    <bind property="home">pyre.home()</property>
    <property name="prefix">pyre.prefix()</property>

    <!-- and some per user settings -->
    <inventory name="user">
      <property name="name">michael a.g. aïvázis</property>
      <property name="email">aivazis@caltech.edu</property>
      <property name="affiliation">california institute of technology</property>
    </inventory>

  </inventory>

</config>


<!-- end of file -->
