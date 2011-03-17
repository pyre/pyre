<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2011 all rights reserved
!
-->

<config>

  <!-- generic configuration for the montecarlo integrator instances -->
  <component family="gauss.integrators.montecarlo">
    <!-- the properties -->
    <bind property="samples">10**5</bind>
    <!-- specify the components -->
    <bind property="mesh">import:gauss.meshes#mersenne</bind>
    <bind property="region">import:gauss.shapes#ball</bind>
  </component>

  <!-- configuration for the example that integrates the gaussian -->
  <component name="mc-gaussian" family="gauss.integrators.montecarlo">
    <!-- specify the components -->
    <bind property="integrand">import:gauss.functors#gaussian</bind>

    <component name="box">
      <bind property="diagonal">((-1,-1), (1,1))</bind>
    </component>

    <component name="integrand" family="gauss.functors.gaussian">
      <bind property="μ">(0,0)</bind>
      <bind property="σ">1/3</bind>
    </component>

  </component>

  <!-- configuration for the example that computes π -->
  <component name="mc-π" family="gauss.integrators.montecarlo">
    <!-- specify the components -->
    <bind property="integrand">import:gauss.functors#one</bind>
  </component>

  <component name="mc-π.box">
    <bind property="diagonal">((0,0),(1,1))</bind>
  </component>

</config>


<!-- end of file -->
