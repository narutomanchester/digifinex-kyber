import requests
import time
import hmac
import hashlib
import urllib
import json
import os
import ast
from eth_account import Account
from dotenv import load_dotenv
import sys
import requests
from web3 import Web3, HTTPProvider
from utils import Utils
load_dotenv()

sys.path.append(os.path.dirname(__file__))

pgx_usdt_pool_contract_address = "0x3f1f398887525d2d9acd154ec5e4a3979adffae6"
pgx_usdt_pool_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"feeInPrecision","type":"uint256"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"vReserve0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"vReserve1","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"reserve0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"reserve1","type":"uint256"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"shortEMA","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"longEMA","type":"uint256"},{"indexed":false,"internalType":"uint128","name":"lastBlockVolume","type":"uint128"},{"indexed":false,"internalType":"uint256","name":"skipBlock","type":"uint256"}],"name":"UpdateEMA","type":"event"},{"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ampBps","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"domainSeparator","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"contract IDMMFactory","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTradeInfo","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint112","name":"_vReserve0","type":"uint112"},{"internalType":"uint112","name":"_vReserve1","type":"uint112"},{"internalType":"uint256","name":"feeInPrecision","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVolumeTrendData","outputs":[{"internalType":"uint128","name":"_shortEMA","type":"uint128"},{"internalType":"uint128","name":"_longEMA","type":"uint128"},{"internalType":"uint128","name":"_currentBlockVolume","type":"uint128"},{"internalType":"uint128","name":"_lastTradeBlock","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_token0","type":"address"},{"internalType":"contract IERC20","name":"_token1","type":"address"},{"internalType":"uint32","name":"_ampBps","type":"uint32"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sync","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"token0","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token1","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

class Kyberswap():
    def __init__(self):
        self.web3 = Web3(HTTPProvider(os.getenv("POLYGON_RPC_URL")))
        self.pool_contract = self.web3.eth.contract(address=Web3.toChecksumAddress(pgx_usdt_pool_contract_address), abi=pgx_usdt_pool_abi)
        self.account = Account.from_key(os.getenv("PRIVATE_KEY"))

    def get_balance_erc20_by_address(self, erc20_contract, account_address: str) :
        return erc20_contract.functions.balanceOf(account_address).call()

    def get_curr_price(self):
        trade_info = self.pool_contract.functions.getTradeInfo().call()
        _vReserve0, _vReserve1 = trade_info[2], trade_info[3]
        return _vReserve1*(10**12)/_vReserve0

    # call Kyber Aggregator API to Get Swap Info 
    def getSwapData(self, usdt_amount_in):
        # load base data
        url = "https://aggregator-api.kyberswap.com/polygon/route/encode"
        params_str = f"""{
                        'tokenIn': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
                        'tokenOut': '0xc1c93d475dc82fe72dbc7074d55f5a734f8ceeae',
                        'amountIn': %d,
                        'saveGas': '0',
                        'gasInclude': '0',
                        'slippageTolerance': '80',
                        'deadline': %d,
                        'to': '%s',
                    }"""%(usdt_amount_in, int(time.time() + 60 * 2), self.account.address)
        params = ast.literal_eval(params_str)
        print(params)

        # call API
        while True:
            try:
                r = requests.get(url, params=params)
                break
            except:
                time.sleep(1)

        return r.json()

    def sign_approve_transaction(self, router_address, amount):

        tx = self.token_in_contract.functions.approve(router_address, amount).buildTransaction({
            'from': self.account.address, 
            'nonce': self.web3.eth.getTransactionCount(self.account.address)
            })
            
        transaction_hash = Utils.sign_transaction(self.web3, tx, self.account.key)
        if not transaction_hash:
            Utils.log_request("apptove tx failed")
            exit(1)
        time.sleep(10)
        return transaction_hash

    def sign_swap_trasaction(self, r: dict):

        tx = {
            "nonce": self.web3.eth.getTransactionCount(self.account.address),
            "from": self.account.address,
            "to": r["routerAddress"],
            "data": r["encodedSwapData"],
            "chainId": 137,
            
            # int(r['totalGas']*1.05),
            "gasPrice": int(self.web3.eth.gasPrice*1.05)
        }
        tx["gas"] = int(self.web3.eth.estimateGas(tx)*1.05)
        # sign
        

        transaction_hash = Utils.sign_transaction(self.web3, tx, self.account.key)
        Utils.log_request(f"tx swap:  {tx}")

        return transaction_hash

    def execute_swap(self, amount_in ):
        
        while True:
            Utils.log_request("Exec Swap " + self.token_in_symbol + " " + self.token_out_symbol + " " + str(self.amount_in/10**int(self.token_in_decimal)) + " " + str(self.min_rate))
            Utils.log_request(f"start exec with wallet: {self.account.address}")

            # get swap info
            r = self.getSwapData(amount_in)
            print(r)

            
            # exec swap
            transaction_hash = self.sign_swap_trasaction(r)

            return transaction_hash


class Digifinex():
    def __init__(self):
        self.appKey = str(os.getenv("DIGIFINEX_APPKEY"))
        self.appSecret = str(os.getenv("DIGIFINEX_APPSECRET"))

    def _generate_accesssign(self, data):
        query_string = urllib.parse.urlencode(data)
        m = hmac.new(self.appSecret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        s = m.hexdigest()
        print("data-origin:", data)
        print("query_string:", query_string)
        print("sign:", s)
        return s

    def do_request(self, method, path, data, needSign=False):
        baseUrl = "https://openapi.digifinex.com/v3"
        if needSign:
            headers = {
                "ACCESS-KEY": self.appKey,
                "ACCESS-TIMESTAMP": str(int(time.time())),
                "ACCESS-SIGN": self._generate_accesssign(data),
            }
        else:
            headers = {}
        if method == "POST":
            response = requests.request(method, baseUrl+path, data=data, headers=headers)
        else:
            response = requests.request(method, baseUrl+path, params=data, headers=headers)
        
        return json.loads(response.text)
        

    def get_curr_price(self):
        price = float(self.do_request("GET", "/ticker", {"symbol": "pgx_usdt",}, True)['ticker'][0]['sell'])

        return price 

    def get_balance(self):
        assets = self.do_request("GET", "/spot/assets", {}, True)['list']
        for asset in assets:
            if asset['currency'] == "PGX":
                return asset['free']

    def create_sell_order(self, base_payload):
        
        # create order
        order_id =  self.do_request("POST", "/spot/order/new", base_payload, True)['order_id']

        return order_id
    
    def get_order_status(self, order_id):
        order_data =  self.do_request("POST", "/spot/order", {'market':'spot', 'order_id': [order_id]}, True)['data']

        return order_data

    def sell(self, amount, price):
        base_payload = {
            "market": "spot",
            "symbol": "PGX_USDT",
            "type": "sell",
            "amount": amount,
            "post_only": 1
        }

        while True:
            # create sell order
            new_base_load = base_payload.copy()
            new_base_load['price'] = price
            order_id = self.create_sell_order(new_base_load)

            # check order filled yet ? 
            order_data = self.get_order_status(order_id)

            # update new price 
            price = price *0.997

            # if already executed 
            if order_data['executed_amount'] > 0 :
                # return executed_amount & amount_out & new price
                return order_data['executed_amount'], order_data['cash_amount'], price



def main():
    # init
    kyber = Kyberswap()
    digifinex = Digifinex()

    # get price
    
    digifinex_price = digifinex.get_curr_price()
    digifinex_balance_pgx = digifinex.get_balance()
    
    while True:
        kyber_price = kyber.get_curr_price()

        diff = digifinex_price/kyber_price

        # log
        Utils.log(f"kyber_price: {kyber_price}, digifinex_price: {digifinex_price}")
        Utils.log(f"diff: {diff}")

        #  If the diff is more than 10%
        # sell pgx on digifinex, buy on kyberswap
        if diff > 1.05 and digifinex_balance_pgx>0:
            # create sell order on digifinex
            executed_amount, cash_amount, digifinex_price = digifinex.sell(min(7000,digifinex_balance_pgx), digifinex_price)
            digifinex_balance_pgx -= executed_amount

            # create buy order on kyberswap with cash amount
            transaction_hash = kyber.execute_swap(cash_amount)


            # log
            log_str = f"Successfully Did Swap {cash_amount} USD in {transaction_hash}" if transaction_hash else "Failed",

            Utils.log_request(log_str)

            Utils.send_message(int(os.getenv("TELEGRAM_GROUP_ID")), 
                                log_str,
                                reply_markup={
                                    "inline_keyboard": [
                                        [
                                            {"text": "Transaction hash", "url": f"https://polygonscan.com/tx/{transaction_hash}"}
                                        ]
                                    ]
                                } if transaction_hash else None)

        else:
            break



main()