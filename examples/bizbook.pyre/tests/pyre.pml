<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2012 all rights reserved
!
-->

<config>

  <!-- some global settings -->
  <component family="pyre.db.server.postgres">
    <bind property="database">postgres</bind>
  </component>

  <!--  settings for particular test cases -->
  <component name="bizbook" family="pyre.db.server.postgres">
    <bind property="database">bizbook</bind>
  </component>

</config>


<!-- end of file -->
