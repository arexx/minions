import logging,os,errno,sys

def drop_permissions():
    logging.debug("Dropping permissions")
    try:
        import pwd
    except ImportError:
        logging.critical('Cannot import module "pwd"')
        sys.exit(1)
    nobody = pwd.getpwnam('nobody')[2]
    try:
        os.setuid(nobody)
    except OSError, e:
        if e.errno != errno.EPERM: raise
        logging.warn('Cannot setuid "nobody"')
        #sys.exit(1)