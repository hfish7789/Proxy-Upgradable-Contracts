import pytest
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, network, exceptions

from scripts.helper_scripts import LOCAL_BLOCKCHAINS, encode_data, get_account, get_contract
from scripts.upgrade_box_contract import upgrade


# test that the proxy delegate the calls to the Box smart contract
def test_proxy_delegated_call():

    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()

    account = get_account()

    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})

    encoded_initializer = encode_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_initializer,
        {"from": account}
    )

    box_proxy = get_contract(Box, proxy.address)

    assert box_proxy.getValue() == box.getValue()

    set_tx = box_proxy.setValue(10, {"from": account})
    set_tx.wait(1)

    assert box_proxy.getValue() == 10

# test that the proxy upgrade to the BoxV2 contract
def test_upgrade_proxy():

    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()

    account = get_account()

    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})

    encoded_initializer = encode_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_initializer,
        {"from": account}
    )
    
    box_proxy = get_contract(Box, proxy.address)

    set_tx = box_proxy.setValue(10, {"from": account})
    set_tx.wait(1)

    box_v2 = BoxV2.deploy({"from": account})

    box_proxy = get_contract(BoxV2, proxy.address)

    with pytest.raises(exceptions.VirtualMachineError):
        set_tx = box_proxy.increment(5, {"from": account})
        set_tx.wait(1)

    upgrade(
        account=account,
        proxy=proxy,
        implementation_address=box_v2.address,
        admin_contract=proxy_admin,
    )

    box_proxy = get_contract(BoxV2, proxy.address)

    assert box_proxy.getValue() == 10

    set_tx = box_proxy.increment(5, {"from": account})
    set_tx.wait(1)

    assert box_proxy.getValue() == 15

