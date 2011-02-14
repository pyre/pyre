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
    <bind property="integrand">import://gauss.functors#gaussian</bind>
    <bind property="region">import://gauss.shapes#ball</bind>

    <component name="box">
      <bind property="diagonal">((-1,-1), (1,1))</bind>
    </component>

  </component>

  <component name="mc.integrand" class="gauss.functors.gaussian">
    <bind property="μ">(0,0)</bind>
    <bind property="σ">1/3</bind>
  </component>

</config>


<!-- end of file -->
