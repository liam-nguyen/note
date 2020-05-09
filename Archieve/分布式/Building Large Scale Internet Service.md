---
title: Building Large Scale Internet Service
toc: false
date: 2017-10-30
---

Building Large Scale Internet Service, Jeff Dean, Google

Typical first year for a new cluster:

* ~1 <hh>network rewiring</hh> (rolling ~5% of machines down over 2-day span) 
* ~20 <hh>rack failures</hh> (40-80 machines instantly disappear, 1-6 hours to get back) 
* ~5 <hh>racks go wonky</hh> (40-80 machines see 50% packet loss) 
* ~8 <hh>network maintenances</hh> (4 might cause ~30-minute random connectivity losses)
*  ~12 <hh>router reloads</hh> (takes out DNS and external vips for a couple minutes) 
*  ~3 <hh>router failures</hh> (have to immediately pull traffic for an hour) 
*  ~dozens of <hh>minor 30-second blips for dns </hh>
*  ~1000 <hh>individual machine failures </hh>
*  ~thousands of <hh>hard drive failures</hh>