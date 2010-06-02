<?xml version="1.0" encoding="utf-8"?>
<!--
!
! michael a.g. aïvázis
! california institute of technology
! (c) 1998-2010  all rights reserved
!
-->

<config>

  <component family="functor">
    <bind property="mean">config - mean</bind>
    <bind property="μ">config - μ</bind>
    <bind property="spread">config - spread</bind>
    <bind property="σ">config - σ</bind>
  </component>

  <component name="gaussian" family="functor">
    <bind property="mean">instance - mean</bind>
    <bind property="μ">instance - μ</bind>
    <bind property="spread">instance - spread</bind>
    <bind property="σ">instance - σ</bind>
  </component>

</config>


<!-- end of file -->
