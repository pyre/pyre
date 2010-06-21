<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2010  all rights reserved
!
-->

<config>

  <!-- configuration for the montecarlo integrator instance -->
  <component name="mc">
    <!-- the properties -->
    <bind property="samples">10**6</bind>
    <!-- specify the components -->
    <bind property="box">import://gauss.shapes#box</bind>
    
  </component>

</config>


<!-- end of file -->
