from ..services import TransactionService
from ..services import AddressService
from ..services import BlockService
from flask import render_template
from flask import Blueprint
from pony import orm

blueprint = Blueprint("frontend", __name__)

@blueprint.route("/")
@orm.db_session
def home():
    blocks = BlockService.blocks(size=100)
    return render_template("pages/overview.html", blocks=blocks)

@blueprint.route("/block/<string:blockhash>")
@orm.db_session
def block(blockhash):
    block = BlockService.get_by_hash(blockhash)
    return render_template("pages/block.html", block=block)

@blueprint.route("/transactions")
@orm.db_session
def transactions():
    transactions = TransactionService.transactions(size=100)
    return render_template("pages/transactions.html", transactions=transactions)

@blueprint.route("/transaction/<string:txid>")
@orm.db_session
def transaction(txid):
    transaction = TransactionService.get_by_txid(txid)
    return render_template("pages/transaction.html", transaction=transaction)

@blueprint.route("/address/<string:address>")
@orm.db_session
def address(address):
    address = AddressService.get_by_address(address)
    return render_template("pages/address.html", address=address)

@blueprint.route("/masternodes")
def masternodes():
    return render_template("layout.html")

@blueprint.route("/holders")
@orm.db_session
def holders():
    richlist = AddressService.richlist()
    return render_template("pages/holders.html", richlist=richlist)

@blueprint.route("/network")
def network():
    return render_template("layout.html")

@blueprint.route("/docs")
def docs():
    return render_template("layout.html")
