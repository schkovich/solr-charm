from charms.reactive import when, when_not, set_state
from charmhelpers.fetch.archiveurl import ArchiveUrlFetchHandler
from subprocess import check_call, CalledProcessError, call, check_output
from charmhelpers.core.hookenv import status_set, log, status_get
from charmhelpers.core import hookenv
from charmhelpers.core.host import adduser, chownr, mkdir

au = ArchiveUrlFetchHandler()

@when_not('solr.installed')
def install_solr():
    adduser('solr')
    au.download("http://apache.claz.org/lucene/solr/6.3.0/solr-6.3.0.tgz", "/tmp/solr.tgz")
    mkdir('/opt/solr')
    check_output(['tar', 'xvfz', "/tmp/solr.tgz", '-C', "/opt/solr", '--strip-components=1'])
    chownr('/opt/solr', 'solr', 'solr', chowntopdir=True)
    set_state('solr.installed')

#@when('zookeeper.joined')
#@when_not('zookeeper.ready')
# need to check for cloud setup
def wait_for_zookeeper(zookeeper):
    """
         We always run in Distributed mode, so wait for Zookeeper to become available.
    """
    hookenv.status_set('waiting', 'Waiting for Zookeeper to become available')

#@when_not('zookeeper.joined')
# need to check for cloud setup
def wait_for_zkjoin():
    """
        Wait for Zookeeper
    """
    status_set('waiting', 'Waiting for Zookeeper to become joined')



@when('solr.installed')
@when('java.ready')
@when_not('zookeeper.ready')
def run_solr(java):
   hookenv.open_port('8983')
   solrcloud = hookenv.config()['solrcloud']
   try:
       check_output(['su','solr','-c','/opt/solr/bin/solr status'])
   except CalledProcessError as e:
       if not solrcloud:
           check_output(['su','solr','-c','/opt/solr/bin/solr start'])
           status_set('active', 'Solr Running(No Cloud).')
           set_state('solr.running')
       else:
           status_set('blocked', 'Waiting for Zookeeper.')


@when('solr.installed')
@when('java.ready')
@when('zookeeper.ready')
def run_solr(zookeeper, java):
    hookenv.open_port('8983')
    solrcloud = hookenv.config()['solrcloud']
    charmstatus = status_get()
    log("CHARMSTAT " + charmstatus[0])
    log("CHARMSTAT " + charmstatus[1])
    # TODO if status returns error then unset solr.running and status_set
    # TODO detect if ZK info changes and restart solr nodes
    if solrcloud and (charmstatus[1] != 'Solr Cloud Running'):
        zklist = ''
        for zk_unit in zookeeper.zookeepers():
            zklist += add_zookeeper(zk_unit['host'], zk_unit['port'])
        zklist = zklist[:-1]
        call(['su','solr','-c','/opt/solr/bin/solr stop'])
        check_output(['su','solr','-c','/opt/solr/bin/solr start -c -p 8983 -z '+zklist])
        status_set('active', 'Solr Cloud Running')
        set_state('solrcloud.running')
    elif not solrcloud and (charmstatus[1] != 'Solr Running(No Cloud)'):
        call(['su','solr','-c','/opt/solr/bin/solr stop'])
        check_output(['su','solr','-c','/opt/solr/bin/solr start'])
        status_set('active', 'Solr Running(No Cloud)')
        set_state('solr.running')


@when('solr-interface.core.requested')
def provide_core(solr):
    for service in solr.requested_cores():
        database = generate_dbname(service)
        solr.provide_core(service=service, host=hookenv.unit_private_ip(), port="8983", core=service)

def generate_dbname(name):
    print(name)

@when_not('java.ready')
def update_java_status():
    status_set('blocked', 'Waiting for Java.')

def add_zookeeper(host, port):
    """
        Return a ZK hostline for the config.
    """
    return host+':'+port+','
