# Overview

Solr Charm for deployment of Apache Solr to Juju.

# Usage

Step by step instructions on using the charm:

    juju deploy cs:~apachesoftwarefoundation/solr --channel edge
    juju deploy openjdk
    juju add-relation openjdk solr
    juju expose solr

You can then browse to http://ip-address:8983 to configure the service.

## Scale out Usage

If the charm has any recommendations for running at scale, outline them in
examples here. For example if you have a memcached relation that improves
performance, mention it here.

## Known Limitations and Issues

Currently doesn't scale, SolrCloud support coming soon.

# Configuration

# Contact Information

Contact the developers here:

## Upstream Project Name

  - https://launchpad.net/~apachesoftwarefoundation
  - https://github.com/buggtb/solr-charm/issues
  - tom@spicule.co.uk

[service]: http://example.com
[icon guidelines]: https://jujucharms.com/docs/stable/authors-charm-icon
