OntCversion = '2.0.0'
'''
Ontology Naming Service Smart Contract
Author: Zhou peiwen
'''

from ontology.builtins import *
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.Ontology.Native import Invoke
from ontology.interop.Ontology.Runtime import Base58ToAddress, AddressToBase58
from ontology.interop.System.Action import RegisterAction
from ontology.interop.System.App import DynamicAppCall
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize,Log
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.libont import str, address2hexstring,mulconcat,split,list_remove_elt,join

adminAddress = Base58ToAddress("ASYkgyWm4GFiXqVKZs6XrjaN3HnFVGRhDs")
ONTID_ADDRESS = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03')
ctx = GetContext()

OWNER_KEY = 'OWNER'
VALID_KEY = 'VALID'
VALUE_KEY = 'VALUE'
RECORDS_KEY = 'RECORDS'
MAX_COUNT = 100

# events:
RegisterDomainEvent = RegisterAction("registerDomain", "domain", "owner","validTo")
UpdateValidPeriodEvent = RegisterAction("updateValidPeriod","domain","newvalid")
DeleteDomainEvent = RegisterAction("deleteDomain","domain")
BindValueEvent = RegisterAction("bindValue","domain","ctype","value")
TransferEvent = RegisterAction("transfer","domain","from","to")

def Main(operation,args):
    if operation == 'registerDomain':
        if len(args) != 4:
            return False
        return registerDomain(args[0],args[1],args[2],args[3])
    if operation == 'updateValidPeriod':
        if len(args)!= 3:
            return False
        return updateValidPeriod(args[0],args[1],args[2])
    if operation == 'deleteDomain':
        if len(args)!= 2:
            return False
        return deleteDomain(args[0],args[1])
    if operation == 'bindValue':
        if len(args)!=4:
            return False
        return bindValue(args[0],args[1],args[2],args[3])
    if operation == 'ownerOf':
        if len(args)!= 1:
            return False
        return ownerOf(args[0])
    if operation == 'validTo':
        if len(args)!= 1:
            return False
        return validTo(args[0])
    if operation == 'valueOf':
        if len(args)!= 1:
            return False
        return valueOf(args[0])
    if operation == 'isDomainValid':
        if len(args)!= 1:
            return False
        return isDomainValid(args[0])    
    if operation == 'transfer':
        if len(args)!=3:
            return False
        return transfer(args[0],args[1],args[2])
    if operation == 'getDomains':
        if len(args) != 1:
            return False
        return getDomains(args[0])
    if operation == 'migrateContract':
        if len(args) != 7:
            return False
        return migrateContract(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
    return False


def registerDomain(fulldomain, registerdid,idx, validto):
    '''
    register domain
    fulldomain: domain string
    registerdid: register ontid
    idx:owner walletid
    validto : valid period
    '''
    currenttime = GetTime()
    if validto > 0:
        assert(validto > currenttime)
    assert(len(fulldomain) > 0)
    _validateDNSName(fulldomain)
    lowerdomain = lower(fulldomain)
    assert(not ownerOf(lowerdomain))
    _checkParentAuth(lowerdomain,idx)

    Put(ctx,_concatkey(OWNER_KEY,lowerdomain),registerdid)
    Put(ctx,_concatkey(VALID_KEY,lowerdomain),validto)

    recordskey = _concatkey(RECORDS_KEY,registerdid)
    records = Get(ctx,recordskey)

    if not records:
        records = [lowerdomain]
    else:
        records = Deserialize(records)
        records.append(lowerdomain) 

    assert(len(records) <= MAX_COUNT)    
    Put(ctx,recordskey,Serialize(records))

    RegisterDomainEvent(lowerdomain,registerdid,validto)
    return True

def updateValidPeriod(fulldomain,idx,validto):
    '''
    update valid period
    fulldomain: domain string
    '''

    assert(len(fulldomain) > 0)
    #domain is exist
    assert(ownerOf(fulldomain))

    lowerdomain = lower(fulldomain)
    _checkParentAuth(lowerdomain,idx)

    Put(ctx,_concatkey(VALID_KEY,lowerdomain),validto)
    UpdateValidPeriodEvent(lowerdomain,validto)
    return True

def deleteDomain(fulldomain,idx):
    '''
    delete domain
    '''
    assert(len(fulldomain) > 0)
    #domain is exist
    owner = ownerOf(fulldomain)
    assert(owner)

    lowerdomain = lower(fulldomain)
    _checkParentAuth(lowerdomain,idx)

    Delete(ctx,_concatkey(OWNER_KEY,lowerdomain))
    Delete(ctx,_concatkey(VALID_KEY,lowerdomain))
    Delete(ctx,_concatkey(VALUE_KEY,lowerdomain))

    recordkey = _concatkey(RECORDS_KEY,owner)
    records = Deserialize(Get(ctx,recordkey))
    records = list_remove_elt(records,lowerdomain)

    if len(records) == 0:
        Delete(ctx,recordkey)
    else:
        Put(ctx,recordkey,Serialize(records))

    DeleteDomainEvent(lowerdomain)
    return True

def bindValue(fulldomain,idx, ctype,inputvalue):
    '''
    bindValue to domain
    '''
    owner = ownerOf(fulldomain)
    assert(_verifyOntid(owner,idx))
    assert(isDomainValid(fulldomain))
    value = [ctype,inputvalue]
    lowerdomain = lower(fulldomain)
    Put(ctx,_concatkey(VALUE_KEY,lowerdomain),Serialize(value))
    BindValueEvent(lowerdomain,ctype,inputvalue)
    return True

def valueOf(fulldomain):
    '''
    value of domain
    '''
    assert(isDomainValid(fulldomain))
    lowerdomain = lower(fulldomain)

    rawvalue = Get(ctx,_concatkey(VALUE_KEY,lowerdomain))
    value = Deserialize(rawvalue)
    return _concatkey(value[0],value[1])


def validTo(fulldomain):
    '''
    valid period of domain
    '''
    lowerdomain = lower(fulldomain)
    return Get(ctx,_concatkey(VALID_KEY,lowerdomain))

def ownerOf(fulldomain):
    '''
    get owner of the domain
    '''
    lowerdomain = lower(fulldomain)
    return Get(ctx,_concatkey(OWNER_KEY,lowerdomain))

def isDomainValid(fulldomain):
    '''
    get domain is valid
    '''
    currenttime = GetTime()
    lowerdomain = lower(fulldomain)

    validto = validTo(lowerdomain)
    if not validto:
        return False
    else:
        if validto > 0:
            return validto >= currenttime

    parent = _getParentDomain(lowerdomain)

    if len(parent) == 0:
        if validto == -1:
            return True
        else:
            return isDomainValid(parent)
    else:
        return isDomainValid(parent)

def transfer(fulldomain,idx,todid):
    '''
    transfer domain to other did
    '''
    assert(len(fulldomain) > 0)
    lowerdomain = lower(fulldomain)
    assert(isDomainValid(lowerdomain))
    owner = ownerOf(lowerdomain)
    assert(_verifyOntid(owner,idx))
    Put(ctx,mulconcat(OWNER_KEY,lowerdomain),todid)

    fromrecordkey = _concatkey(RECORDS_KEY,owner)
    fromrecords = Deserialize(Get(ctx,fromrecordkey))
    fromrecords = list_remove_elt(fromrecords,lowerdomain)
    if len(fromrecords) == 0:
        Delete(ctx,fromrecordkey)
    else:
        Put(ctx,fromrecordkey,Serialize(fromrecords))

    torecordkey = _concatkey(RECORDS_KEY,todid)
    torecordsRaw = Get(ctx,torecordkey)
    if not torecordsRaw:
        torecords = [lowerdomain]
        Put(ctx,torecordkey,Serialize(torecords))
    else:
        torecords = Deserialize(torecordsRaw)
        torecords.append(lowerdomain)
        assert(len(torecords) <= MAX_COUNT)    
        Put(ctx,torecordkey,Serialize(torecords))


    TransferEvent(fulldomain,owner,todid)

    return True

def getDomains(did):
    '''
    get domains owned by did
    '''
    reocordsRaw = Get(ctx,_concatkey(RECORDS_KEY,did))
    if not reocordsRaw:
        return ''
    else:
        records = Deserialize(reocordsRaw)
        return join(',',records)


## DO REMEMBER transfer all asset before call migrate
def migrateContract(code, needStorage, name, version, author, email, description):
    assert (CheckWitness(adminAddress))
    res = Migrate(code, needStorage, name, version, author, email, description)
    assert (res)
    Notify(["migrateContract", adminAddress, GetTime()])
    return True




def _concatkey(str1, str2):
    return mulconcat(str1,"_",str2)

def _verifyOntid(ont_id, index):
    return  Invoke(0, ONTID_ADDRESS, "verifySignature", state(ont_id, index))

def _checkParentAuth(lowerdomain,idx):
    tmp = split(lowerdomain,'.')
    if len(tmp) == 1:
        #top domain case
        #check the admin sig
        assert(CheckWitness(adminAddress))
    elif len(tmp) == 2:
        #a.ont case
        parent = tmp[1]
        parentowner = ownerOf(parent)
        assert(_verifyOntid(parentowner,idx))
    elif len(tmp) == 3:
        #a.b.ont case
        parent = mulconcat(tmp[1],".",tmp[2]) 
        parentowner = ownerOf(parent)
        assert(_verifyOntid(parentowner,idx))
    else:
        # *.a.b.ont case 
        i = len(tmp) - 3
        parent = mulconcat( tmp[i],".",tmp[i+1],".",tmp[i+2]) 
        parentowner = ownerOf(parent)
        assert(_verifyOntid(parentowner,idx))
    return True

def _getParentDomain(lowerdomain):
    tmp = split(lowerdomain,'.')
    if len(tmp) == 1:
        return ''
    if len(tmp) == 2:
        return tmp[1]
    if len(tmp) == 3:
        return mulconcat(tmp[1],".",tmp[2])
    else:
        i = len(tmp) - 3
        return  mulconcat( tmp[i],".",tmp[i+1],".",tmp[i+2])


def _validateDNSName(domain):
    assert(len(domain) > 0)
    lowerdomain = lower(domain)
    assert(len(domain) <= 253)
    tmp = split(lowerdomain,'.')
    for d in tmp:
        assert(len(d) < 63)

def lower(s):
    res = ''
    delt = 'a' - 'A'
    len_t = len(s)
    for i in range(len_t):
        if 'A' <= s[i:i+1] <= 'Z':
            t = s[i:i+1] + delt
            t = concat(t, b'\x00')
            res = concat(res, t[0:1])
        else:
            res = concat(res, s[i:i+1])

    return res
