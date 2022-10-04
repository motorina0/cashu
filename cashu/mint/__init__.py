from cashu.core.settings import MINT_PRIVATE_KEY
from cashu.mint.business.ledger import Ledger

ledger = Ledger(MINT_PRIVATE_KEY, "data/mint")
