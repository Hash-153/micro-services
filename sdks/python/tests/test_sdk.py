from novacommerce import NovaCommerceClient, Money, Currency

def test_sdk_instantiation():
    client = NovaCommerceClient(base_url="http://localhost:8000")
    assert client.base_url == "http://localhost:8000"
    m = Money(amount=1999, currency=Currency.USD)
    assert m.amount == 1999
