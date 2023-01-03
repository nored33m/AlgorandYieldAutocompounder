# None of this is running yet so bear with me, i'm learning sirs.

from pyteal import *
from beaker import *

# The first few blocks at the beginning here are from following a tutorial, just ignore all of this for about a week.

class Autocompounder(Application):
    
    user_address = ApplicationStateValue(stack_type=TealType.bytes)

    yield_farm_address = ApplicationStateValue(stack_type=TealType.bytes)

    compounding_period = ApplicationStateValue(stack_type=TealType.uint64)

    rewards_during_period = ApplicationStateValue(stack_type=TealType.uint64)

    def create(self):
        return Seq(
            self.user_address.set(Txn.sender()),
            self.yield_farm_address.set(Bytes("")),
            self.compounding_period.set(Int(0)),
            self.rewards_during_period.set(Int(0))

        )
    # Start Auto-Compounder
    @external
        def start_auto_compounder(self):
            # fund the contract with 100k microalgos
            # set the compounding period
            # begin the logic
            self.compounding_period.set(Global.latest_timestamp()+ Length.get()),
    # user: a
    # Yield Farm: address
 Assert(payment.reciever == Global.current_application_address()))
    # create the contract
    # start auto-compounder
    #



# Some random code I made following a tutorial

def approval_program():
    return Seq(
        Log(Bytes("Hello World")),
        Return(Int(1))
    )

    print(compileTeal(approval_program(), Mode.Application, version=6))



# This block of code takes a transaction id and a pre-defined time period as input and calculates the amount
# of funds transferred from the yield farm to the user address over that time period.


def transferred_funds(txn, user_address, start_time, end_time):
    # Check if the transaction is a payment transaction
    is_payment = Txn.application_id(b'payment')
    txn_type_check = Txn.type_enum().eq(is_payment)

    # Check if the transaction is between the external wallet and the user wallet
    sender_check = Txn.sender().eq(user_address)
    receiver_check = Txn.receiver().ne(user_address)
    external_wallet_check = And(sender_check, receiver_check)

    # Check if the transaction was made within the specified time period
    time_check = Txn.close_time().gte(start_time).and_(Txn.close_time().lt(end_time))

    # Return the amount transferred if all conditions are met
    return If(And(txn_type_check, external_wallet_check, time_check), Txn.amount(), 0)

  
# This function takes the amount outputted by the last block and swaps half to a pre-defined ASA minus the tx fee
# For the swap.


def swap_funds(amount, asa_id, fee):
    # Calculate the amount to swap
    swap_amount = amount / 2

    # Check if there are sufficient funds to cover the swap and the transaction fee
    funds_check = Txn.account_balance().gte(swap_amount + fee)

    # Swap the funds and subtract the transaction fee
    swap_and_fee = asa_id.opt_asset_transfer(swap_amount, fee)

    # Return the swap and fee action if there are sufficient funds, otherwise return no action
    return If(funds_check, swap_and_fee, NoOp())

  
# This block of code prepares the funds for yield farming and calls the yield
# farm contract.


def yield_farm(asa_amount, other_asset_amount, yield_farm_contract, user_address):
    # Calculate the difference between the ASA and other asset balances
    balance_difference = Txn.account_balance(asa_id).sub(other_asset_amount)

    # If the ASA balance is greater than the other asset balance, transfer the excess other asset back to the user's wallet
    transfer_excess = other_asset_id.opt_asset_transfer(balance_difference.abs(), 0).to(user_address.opt_asset_transfer(balance_difference.abs(), 0))

    # Call the yield farming contract with the ASA and other asset
    farm = yield_farm_contract.opt_contract_call(asa_id, asa_amount, other_asset_id, other_asset_amount)

    # Return the transfer and farm actions
    return transfer_excess.to(farm)

  
# This block of code loops the program indefinitely and feeds the variables to the various functions
# as long as all conditions are met.


def main():
    # Define the time period for the transferred_funds function
    time_period = 7 * 24 * 60 * 60

    # Define the transaction fee for the swap_funds function
    fee = 500

    # Define the ID of the ASA for the swap_funds and yield_farm functions
    asa_id = AssetId(...)

    # Define the address of the yield farming contract for the yield_farm function
    yield_farm_contract = Address(...)

    # Define the user's wallet address for the yield_farm function
    user_address = Address(...)

    # Define the other asset ID for the yield_farm function
    other_asset_id = AssetId(...)

    # Define the stake asset ID for the stake_funds function
    stake_asset_id = AssetId(...)

    # Define a loop that repeatedly calls the transferred_funds, swap_funds, and yield_farm functions
    loop = Loop(
        # Call the transferred_funds function and store the result in a variable
        transferred_funds(time_period).set_var("amount"),
        # Call the swap_funds function with the amount from the transferred_funds function and the ASA ID and fee
        swap_funds(Var("amount"), asa_id, fee),
        # Call the yield_farm function with the ASA amount and other asset amount from the transferred_funds function, the yield farming contract, and the user's wallet address
        yield_farm(Var("amount"), Var("amount"), yield_farm_contract, user_address)
    )

    # Return the loop
    return loop









