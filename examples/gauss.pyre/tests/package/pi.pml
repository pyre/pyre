<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2011 all rights reserved
!
-->

<config>

  <!-- configuration for the montecarlo integrator instance -->
  <component name="mc">
    <!-- the properties -->
    <bind property="samples">10**5</bind>
    <!-- specify the components -->
    <bind property="mesh">import://gauss.meshes#mersenne</bind>
    <bind property="integrand">import://gauss.functors#one</bind>
    <bind property="region">import://gauss.shapes#ball</bind>
  </component>

  <component name="mc.box">
    <bind property="diagonal">((0,0),(1,1))</bind>
  </component>

</config>


<!-- end of file -->
