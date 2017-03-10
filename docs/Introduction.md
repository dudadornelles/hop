## Introduction

Welcome to hop. Hop was created to speed up the process of provisioning, managing and configuring [GoCD](https://go.cd) through code.

Hop has three main concepts:

* Providers: a provider manages the lifecycle of the GoCD server and agents. It is a plugin system, so you can decide what to use as 
the underlying infrastructure by chosing/implementing a provider. Currently `hop` ships with a `local_docker` provider, that uses a
local docker socket to spin up the server and agents in your local docker daemon.  
* Plans: plans are an abstraction one-level higher then GoCD's pipelines. A plan is a collection of 1 or more pipelines. Plans are also 
a plugin system and are written in python using the [gomatic](https://github.com/SpringerSBM/gomatic) library. 
* Apps: apps or 'app definitions' are data structures with a 'plan', that get processed and transformed into pipelines. 

Hop is specially valuable for platforms where there are 'categories' of applications (that get built/deployed in similar ways), for now
you can define a 'plan' to represent a 'category' and thus streamline the process of creating and (most important) deploying new applications.
