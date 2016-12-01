from charms.reactive import when, when_not, set_state
from charmhelpers.fetch.archiveurl import ArchiveUrlFetchHandler
from subprocess import check_call, CalledProcessError, call, check_output
from charmhelpers.core.hookenv import status_set, log
from charmhelpers.core import hookenv

au = ArchiveUrlFetchHandler()

@when_not('solr.installed')
def install_solr():
    au.download("http://apache.claz.org/lucene/solr/6.3.0/solr-6.3.0.tgz", "/tmp/solr.tgz")
    check_output(['tar', 'xvfz', "/tmp/solr.tgz", '-C', "/opt/"])
    set_state('solr.installed')

@when('solr.installed')
@when('java.ready')
@when_not('solr.running')
def run_solr(java):
   hookenv.open_port('8983')
   check_output(['/opt/solr-6.3.0/bin/solr', 'start', '-force'])
   status_set('running', 'Solr Running.')
   set_state('solr.running')


@when_not('java.ready')
def update_java_status():
    status_set('blocked', 'Waiting for Java.')

