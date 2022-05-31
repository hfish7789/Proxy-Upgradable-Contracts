from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, network
from scripts.helper_scripts import get_account, encode_data, get_contract

def upgrade(
    account, 
    proxy, 
    implementation_address, 
    admin_contract=None, 
    initializer=None, 
    *args
    ):
    if admin_contract:
        if initializer:
            encoded_initiializer = encode_data(initializer, *args)
            transaction = admin_contract.upgradeAndCall(
                proxy.address,
                implementation_address,
                encoded_initiializer,
                {"from": account}
            )
        else: 
            transaction = admin_contract.upgrade(
                proxy.address,
                implementation_address,
                {"from": account}
            )
    else:
        if initializer:
            encoded_initiializer = encode_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                implementation_address,
                encoded_initiializer,
                {"from": account}
            )
        else: 
            transaction = proxy.upgradeTo(
                implementation_address,
                {"from": account}
            )
    return transaction

def main():
    account = get_account()

    # deploy first version of Box contract
    box = Box.deploy({"from": account})

    print(box.getValue())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    #initializer is used to initialize all the values of all variable in a smart contract
    # initializer = box.setValue, 1
    encoded_initializer = encode_data()

    # proxy contract is used to redirect calls to the latest version of the given smart contract
    # deploy the proxy contract
    upgradable_proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_initializer,
        {"from": account}
    )

    print(f"proxy deployed at {upgradable_proxy.address}")

    # get the latest Box contract stored in the proxy
    proxy_box = get_contract(Box, upgradable_proxy.address)

    set_tx = proxy_box.setValue(9, {"from": account})
    set_tx.wait(1)

    print(f"value is: {proxy_box.getValue()}")

    # deploy the new version of Box contract
    box_v2 = BoxV2.deploy({"from": account})

    # upgrade the Box to BoxV2 in the proxy
    # proxy will now redirect all calls to the BoxV2 contract
    upgrade(account, upgradable_proxy, box_v2.address, proxy_admin)

    print("proxy has been upgraded")

    # get the latest Box contract stored in the proxy
    proxy_box = get_contract(BoxV2, upgradable_proxy.address)

    # use the new function increment from BoxV2
    inc_tx = proxy_box.increment(1, {"from": account})
    inc_tx.wait(1)

    print(f"value is: {proxy_box.getValue()}")
