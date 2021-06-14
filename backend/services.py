from .constants import CURRENCY, BURN_ADDRESS
from .models import Transaction
from .models import Masternode
from .models import Location
from .models import Address
from .models import Balance
from .models import Output
from .models import Input
from .models import Block
from .models import Stats
from .models import Peer
from pony import orm

class BlockService(object):
    @classmethod
    def latest_block(cls):
        return Block.select().order_by(
            orm.desc(Block.height)
        ).first()

    @classmethod
    def create(cls, blockhash, height, created,
               merkleroot, version, stake,
               nonce, size, bits):
        return Block(
            blockhash=blockhash, height=height, created=created,
            merkleroot=merkleroot, version=version, stake=stake,
            nonce=nonce, size=size, bits=bits
        )

    @classmethod
    def get_by_hash(cls, bhash):
        return Block.get(blockhash=bhash)

    @classmethod
    def get_by_height(cls, height):
        try:
            return Block.get(height=height)
        except ValueError:
            return None

    @classmethod
    def blocks(cls, page=1, size=100):
        return Block.select().order_by(
            orm.desc(Block.height)
        ).page(page, pagesize=size)

class TransactionService(object):
    @classmethod
    def get_by_txid(cls, txid):
        return Transaction.get(txid=txid)

    @classmethod
    def create(cls, txid, locktime, size, block,
               coinbase=False, coinstake=False):
        return Transaction(
            txid=txid, locktime=locktime, size=size,
            coinbase=coinbase, coinstake=coinstake,
            block=block
        )

    @classmethod
    def count(cls):
        return Transaction.select().count(distinct=False)

    @classmethod
    def transactions(cls, page=1, currency=None, size=100):
        # query = orm.select((o.transaction, sum(o.amount), o.transaction.id) for o in Output if o.currency == currency).distinct()
        # query = query.order_by(-3)
        query = orm.select(t for t in Transaction)

        if currency:
            query = query.filter(lambda t: currency in t.currencies)

        query = query.order_by(-1)

        return query.page(page, pagesize=size)

class InputService(object):
    @classmethod
    def create(cls, sequence, n, transaction, vout):
        return Input(
            sequence=sequence, transaction=transaction,
            vout=vout, n=n,
        )

class AddressService(object):
    @classmethod
    def get_by_address(cls, script, create=False):
        address = Address.get(address=script)

        if not address and create:
            address = AddressService.create(script)

        return address

    @classmethod
    def richlist(cls, page=1, size=100, currency=CURRENCY):
        query = orm.select(
            (b.address, b.balance) for b in Balance
            if b.currency == currency and b.address.address != BURN_ADDRESS
        )

        query = query.order_by(-2)

        return query.page(page, pagesize=size)

    @classmethod
    def create(cls, address):
        return Address(address=address)

class BalanceService(object):
    @classmethod
    def get_by_currency(cls, address, currency):
        balance = Balance.get(
            address=address, currency=currency
        )

        if not balance:
            balance = BalanceService.create(address, currency)

        return balance

    @classmethod
    def create(cls, address, currency):
        return Balance(
            address=address, currency=currency
        )

class OutputService(object):
    @classmethod
    def get_by_prev(cls, transaction, n):
        return Output.get(transaction=transaction, n=n)

    @classmethod
    def create(cls, transaction, amount, category, address, raw, n,
               currency=CURRENCY):
        return Output(
            transaction=transaction, amount=amount, category=category,
            address=address, raw=raw, n=n, currency=currency
        )

class StatsService(object):
    @classmethod
    def get_by_key(cls, key):
        entry = Stats.get(key=key)

        if not entry:
            entry = Stats(
                key=key
            )

        return entry

class PeerService(object):
    @classmethod
    def list(cls, all_peers=False):
        peers = Peer.select()

        if not all_peers:
            peers = peers.filter(lambda p: p.active is True)

        return peers

    @classmethod
    def get_by_address(cls, address):
        peer = Peer.get(address=address)
        return peer

    @classmethod
    def create(cls, address, port, version, subver, active=True):
        return Peer(
            address=address, port=port, version=version,
            subver=subver, active=active
        )

    @classmethod
    def location(cls, country, lat, lon, city, code, peer):
        return Location(
            country=country, lat=lat, lon=lon,
            city=city, code=code, peer=peer
        )

class MasternodeService(object):
    @classmethod
    def list(cls, all_masternodes=False):
        masternodes = Masternode.select()

        if not all_masternodes:
            masternodes = masternodes.filter(lambda m: m.active is True)

        return masternodes

    @classmethod
    def get_by_address(cls, address):
        masternode = Masternode.get(address=address)
        return masternode

    @classmethod
    def create(cls, rank, activetime, lastseen, lastpaid,
               version, address, txhash, outidx, status,
               pubkey, active=True):
        return Masternode(
            rank=rank, activetime=activetime, lastseen=lastseen,
            lastpaid=lastpaid, version=version, address=address,
            txhash=txhash, outidx=outidx, status=status,
            pubkey=pubkey, active=active
        )
