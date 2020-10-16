草稿 =！！！！！！


Paradigm: In science, a *paradigm* describes distinct concepts or thought patterns in some scientific discipline

Main programming paradigms:

* imperative programming
* functional programming
* logical programming

Orthogonal to it:

* object-oriented programming


Imperative programming is about

* modifying mutable variables
* using assignments
* and control structures such as if-then-else, loops, break, continue, return

The most common informal way to understand imperative programs is as instruction sequences for a Von Neumann computer.

There is a strong correspondence between

Mutable variables $\approx$ memory cells
Variable deferences $\approx$ load instructions
Variable assignments $\approx$ store instructions
Control structures $\approx$ jumps

Problem: Scaling up. How can we avoid conceptualizing programs word by word?

In the end, pure imperative programming is limited by the "Von Neumann" bottleneck:

> One tends to conceptualize data structures word-by-word.

We need other techniques for. defining high-level abstractions such as collections, polynomials, geometric shapes, strings, documents.

Ideally: Develop *theories* of collections, shapes, strings,...