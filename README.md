# Overview

Solr Charm for deployment of Apache Solr to Juju.
Solr is the popular, blazing-fast, open source enterprise search platform built on Apache Lucene.

# Usage

Step by step instructions on using the charm:

    juju deploy cs:~spiculecharms/apache-solr
    juju deploy openjdk
    juju add-relation openjdk solr
    juju expose solr

You can then browse to http://ip-address:8983 to configure the service.

## Scale out Usage

You can also run Solr in SolrCloud mode by attaching it to zookeeper

    juju deploy apache-zookeeper
    juju add-relation apache-zookeeper solr
    juju config solr solrcloud=true

## Known Limitations and Issues

Probably lots.

# Configuration

## SolrCloud

This is the scalable version of Solr, to enable it you need to set this configuration option then connect it to a zookeeper quorum.

# Contact Information

Contact the developers here:

## Upstream Project Name

  - https://launchpad.net/~spiculecharms
  - https://github.com/buggtb/solr-charm/issues
  - tom@spicule.co.uk

[service]: http://example.com
[icon guidelines]: https://jujucharms.com/docs/stable/authors-charm-icon
