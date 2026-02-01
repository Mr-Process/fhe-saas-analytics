# Research on Fully Homomorphic Encryption Libraries# Research on Fully Homomorphic Encryption Libraries

## Introduction

Fully Homomorphic Encryption (FHE) allows computation on encrypted data without decrypting it. This capability enables privacy preserving analytics and AI workflows, but practical implementations require careful library choice. This document summarises leading FHE libraries relevant to our SaaS analytics service.

## OpenFHE

OpenFHE is a comprehensive open source library created by researchers behind PALISADE, HElib, HEAAN and FHEW. It supports multiple FHE schemes—BGV, BFV, CKKS, DM (FHEW) and CGGI (TFHE)—and is designed for both usability and performance【569691000738328†L77-L88】.  A partnership between Intel and Duality introduced a composite scaling mode for the CKKS scheme and an interactive two party bootstrapping protocol, improving precision and enabling multi party computations【291325892316878†L122-L154】.  OpenFHE can compile to WebAssembly, allowing client side FHE in browsers and mobile apps【291325892316878†L155-L160】.  The library integrates with hardware accelerators and complies with HomomorphicEncryption.org post quantum security standards【569691000738328†L77-L88】.

**Strengths:** comprehensive scheme support; active development; hardware and WebAssembly acceleration; multi party bootstrapping; BSD like license.

**Weaknesses:** complexity; compiled C++/Python API; still emerging ecosystem compared to SEAL.

## Microsoft SEAL

Microsoft SEAL is an open source (MIT licence) library that makes homomorphic encryption easy to use.  It provides a simple API and detailed examples and allows computations to be performed directly on encrypted data【563232362082241†L140-L175】.  SEAL supports CKKS and BGV schemes【569691000738328†L94-L104】 and is maintained by Microsoft Research with strong community support【569691000738328†L94-L108】.  Its design emphasises ease of integration into end”to”end encrypted storage and computation services, so customers never share their keys with the service provider【563232362082241†L140-L175】.

**Strengths:** enterprise ready security; straightforward API; extensive documentation and examples; active maintenance; good for integration with Microsoft infrastructure.

**Weaknesses:** fewer schemes (only CKKS and BGV); limited hardware acceleration; performance can lag behind OpenFHE for some workloads.

## Lattigo

Lattigo is an open source Go library implementing Ring‑Learning‑With‑Errors–based homomorphic encryption primitives.  It implements the BFV, BGV and CKKS schemes and provides multi party versions of each scheme【39771032274786†L46-L54】.  The CKKS implementation includes bootstrapping, enabling iterative circuits on encrypted data【39771032274786†L46-L54】.  Lattigo emphasises secure multiparty computation; all schemes include distributed key generation and joint decryption protocols【39771032274786†L46-L54】.  The project began at EPFL and is now maintained by Tune Insight, supported by an advisory committee【39771032274786†L30-L63】.

**Strengths:** written in Go (memory safe and easy to deploy); multi party protocols; supports bootstrapping; active research community.

**Weaknesses:** smaller ecosystem and tooling; less mature than OpenFHE and SEAL; Go language may be unfamiliar to some developers.

## TFHE (Fast Fully Homomorphic Encryption over the Torus)

TFHE is a C/C++ library optimised for fast bootstrapping and binary circuit evaluation.  It implements a fast gate‑by‑gate bootstrapping scheme that allows the homomorphic evaluation of arbitrary Boolean circuits【306436540408376†L43-L58】.  The library supports 10 binary gates (AND, OR, XOR, NAND, NOR, etc.) and a MUX gate, achieving about 76 gates per second per core【306436540408376†L45-L74】.  TFHE allows any number of gates without restricting circuit depth【306436540408376†L55-L58】.  It includes utilities to generate secret/cloud key sets and perform encryption, decryption and homomorphic gate evaluation【306436540408376†L64-L74】.

**Strengths:** extremely fast bootstrapping for Boolean circuits; no restriction on circuit depth; open”source (Apache 2.0); good for binary logic and bitwise operations.

**Weaknesses:** focuses on Boolean gates rather than arithmetic; not ideal for real”number computations; requires careful circuit design; limited to C/C++.

## HElib

HElib is an older C++ library developed by IBM that implements BGV and CKKS schemes with optimisations such as ciphertext packing and key”switching.  It is primarily used in research and academic projects【569691000738328†L154-L160】.  HElib supports bootstrapping and includes several performance optimisations, but its API is less user”friendly than SEAL or OpenFHE.  It is available under the Apache 2.0 licence.

**Strengths:** mature library with BGV/CKKS support; includes advanced optimisations; suitable for academic research.

**Weaknesses:** limited documentation; complex API; slower development pace.

## Other players

Emerging tools include Apple’s Swift Homomorphic Encryption (native Swift library with BFV scheme) and Zama’s Concrete‑ML (privacy‟preserving machine learning framework)【569691000738328†L110-L139】.  Google’s HEIR is a compiler toolchain for FHE rather than a library, aimed at hardware designers and compiler engineers【569691000738328†L141-L149】.  Specialised libraries like cuFHE offer CUDA”accelerated FHE for GPU”heavy workloads【569691000738328†L154-L160】 and fhEVM targets confidential smart contracts【569691000738328†L154-L160】.

## Recommendations for our project
## Project Goal

Based on our research into leading FHE libraries, the goal of the FHE‑SaaS‑Analytics project is to build a production‑ready privacy‑preserving analytics service that:

- Leverages OpenFHE as the primary backend for homomorphic operations due to its comprehensive scheme support and developer-friendly APIs ([TFHE Fast Fully Homomorphic Encryption over the Torus](https://tfhe.github.io/#:~:text=,BFV%2C%20CKKS%2C%20TFHE%20and%20FHEW), [Performance Comparison of Homomorphic Encrypted ...](https://proceedings-of-deim.github.io/DEIM2023/5b-9-2.pdf#:~:text=AU%20)).  
- Provides modular interfaces to experiment with other libraries (e.g., Microsoft SEAL for fast approximate arithmetic or TFHE‑rs for boolean circuits) so that future optimisations can be evaluated.  
- Offers an easy‑to‑use client SDK that hides FHE complexities and exposes simple functions for key generation, encryption, weighted‑sum computation, and decryption.  
- Is designed with economic drivers in mind: pricing plans that reflect the premium value of privacy‑preserving computation, automated onboarding to minimise customer acquisition cost, and product stickiness that maximises lifetime value.

This document will be kept up to date as the project evolves.


For a privacy‟preserving SaaS analytics service, we need a library that supports real”number computations, scalable performance and ease of integration.  OpenFHE and Microsoft SEAL stand out.  OpenFHE provides the most comprehensive feature set—including support for multiple schemes, hardware acceleration and two”party bootstrapping【569691000738328†L77-L88】【291325892316878†L122-L154】—making it ideal for a service that may evolve over time.  Microsoft SEAL offers a simpler API and strong community support【563232362082241†L140-L175】; it could be an alternative for rapid prototyping or where integration with Microsoft services is beneficial.  Lattigo is attractive for Go”based architectures and multi”party scenarios【39771032274786†L46-L54】, while TFHE is best for Boolean logic use”cases【306436540408376†L45-L74】.  HElib remains a solid research tool but lacks the usability we need.  Given our SaaS analytics needs, OpenFHE is recommended as the primary FHE backend, with SEAL as a secondary option for prototyping.


## Introduction

Fully Homomorphic Encryption (FHE) allows computation on encrypted data without decrypting it. This capability enables privacy‑preserving analytics and AI workflows, but practical implementations require careful library choice. This document summarises leading FHE libraries relevant to our SaaS analytics service.

## OpenFHE

OpenFHE is a comprehensive open‑source library created by researchers behind PALISADE, HElib, HEAAN and FHEW. It supports multiple FHE schemes—BGV, BFV, CKKS, DM (FHEW) and CGGI (TFHE)—and is designed for both usability and performance【569691000738328†L77-L88】.  A partnership between Intel and Duality introduced a composite scaling mode for the CKKS scheme and an interactive two‑party bootstrapping protocol, improving precision and enabling multi‑party computations【291325892316878†L122-L154】.  OpenFHE can compile to WebAssembly, allowing client‑side FHE in browsers and mobile apps【291325892316878†L155-L160】.  The library integrates with hardware accelerators and complies with HomomorphicEncryption.org post‑quantum security standards【569691000738328†L77-L88】.

**Strengths:** comprehensive scheme support; active development; hardware and WebAssembly acceleration; multi‑party bootstrapping; BSD‑like license.

**Weaknesses:** complexity; compiled C++/Python API; still emerging ecosystem compared to SEAL.

## Microsoft SEAL

Microsoft SEAL is an open‑source (MIT licence) library that makes homomorphic encryption easy to use.  It provides a simple API and detailed examples and allows computations to be performed directly on encrypted data【563232362082241†L140-L175】.  SEAL supports CKKS and BGV schemes【569691000738328†L94-L104】 and is maintained by Microsoft Research with strong community support【569691000738328†L94-L108】.  Its design emphasises ease of integration into end‑to‑end encrypted storage and computation services, so customers never share their keys with the service provider【563232362082241†L140-L175】.

**Strengths:** enterprise‑ready security; straightforward API; extensive documentation and examples; active maintenance; good for integration with Microsoft infrastructure.

**Weaknesses:** fewer schemes (only CKKS and BGV); limited hardware acceleration; performance can lag behind OpenFHE for some workloads.

## Lattigo

Lattigo is an open‑source Go library implementing Ring‑Learning‑With‑Errors–based homomorphic encryption primitives.  It implements the BFV, BGV and CKKS schemes and provides multi‑party versions of each scheme【39771032274786†L46-L54】.  The CKKS implementation includes bootstrapping, enabling iterative circuits on encrypted data【39771032274786†L46-L54】.  Lattigo emphasises secure multiparty computation; all schemes include distributed key generation and joint decryption protocols【39771032274786†L46-L54】.  The project began at EPFL and is now maintained by Tune Insight, supported by an advisory committee【39771032274786†L30-L63】.

**Strengths:** written in Go (memory‑safe and easy to deploy); multi‑party protocols; supports bootstrapping; active research community.

**Weaknesses:** smaller ecosystem and tooling; less mature than OpenFHE and SEAL; Go language may be unfamiliar to some developers.

## TFHE (Fast Fully Homomorphic Encryption over the Torus)

TFHE is a C/C++ library optimised for fast bootstrapping and binary circuit evaluation.  It implements a fast gate‑by‑gate bootstrapping scheme that allows the homomorphic evaluation of arbitrary Boolean circuits【306436540408376†L43-L58】.  The library supports 10 binary gates (AND, OR, XOR, NAND, NOR, etc.) and a MUX gate, achieving about 76 gates per second per core【306436540408376†L45-L74】.  TFHE allows any number of gates without restricting circuit depth【306436540408376†L55-L58】.  It includes utilities to generate secret/cloud key sets and perform encryption, decryption and homomorphic gate evaluation【306436540408376†L64-L74】.

**Strengths:** extremely fast bootstrapping for Boolean circuits; no restriction on circuit depth; open‑source (Apache 2.0); good for binary logic and bitwise operations.

**Weaknesses:** focuses on Boolean gates rather than arithmetic; not ideal for real‑number computations; requires careful circuit design; limited to C/C++.

## HElib

HElib is an older C++ library developed by IBM that implements BGV and CKKS schemes with optimisations such as ciphertext packing and key‑switching.  It is primarily used in research and academic projects【569691000738328†L154-L160】.  HElib supports bootstrapping and includes several performance optimisations, but its API is less user‑friendly than SEAL or OpenFHE.  It is available under the Apache 2.0 licence.

**Strengths:** mature library with BGV/CKKS support; includes advanced optimisations; suitable for academic research.

**Weaknesses:** limited documentation; complex API; slower development pace.

## Other players

Emerging tools include Apple’s Swift Homomorphic Encryption (native Swift library with BFV scheme) and Zama’s Concrete‑ML (privacy‑preserving machine learning framework)【569691000738328†L110-L139】.  Google’s HEIR is a compiler toolchain for FHE rather than a library, aimed at hardware designers and compiler engineers【569691000738328†L141-L149】.  Specialised libraries like cuFHE offer CUDA‑accelerated FHE for GPU‑heavy workloads【569691000738328†L154-L160】 and fhEVM targets confidential smart contracts【569691000738328†L154-L160】.

## Recommendations for our project

For a privacy‑preserving SaaS analytics service, we need a library that supports real‑number computations, scalable performance and ease of integration.  OpenFHE and Microsoft SEAL stand out.  OpenFHE provides the most comprehensive feature set—including support for multiple schemes, hardware acceleration and two‑party bootstrapping【569691000738328†L77-L88】【291325892316878†L122-L154】—making it ideal for a service that may evolve over time.  Microsoft SEAL offers a simpler API and strong community support【563232362082241†L140-L175】; it could be an alternative for rapid prototyping or where integration with Microsoft services is beneficial.  Lattigo is attractive for Go‑based architectures and multi‑party scenarios【39771032274786†L46-L54】, while TFHE is best for Boolean logic use‑cases【306436540408376†L45-L74】.  HElib remains a solid research tool but lacks the usability we need.  Given our SaaS analytics needs, OpenFHE is recommended as the primary FHE backend, with SEAL as a secondary option for prototyping.
