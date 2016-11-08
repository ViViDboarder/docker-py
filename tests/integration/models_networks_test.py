import docker
from .. import helpers
from .base import BaseIntegrationTest


class ImageCollectionTest(BaseIntegrationTest):

    def test_create(self):
        client = docker.from_env()
        name = helpers.random_name()
        network = client.networks.create(name, labels={'foo': 'bar'})
        self.tmp_networks.append(network.id)
        assert network.name == name
        assert network.attrs['Labels']['foo'] == "bar"

    def test_get(self):
        client = docker.from_env()
        name = helpers.random_name()
        network_id = client.networks.create(name).id
        self.tmp_networks.append(network_id)
        network = client.networks.get(network_id)
        assert network.name == name

    def test_list_remove(self):
        client = docker.from_env()
        name = helpers.random_name()
        network = client.networks.create(name)
        self.tmp_networks.append(network.id)
        assert network.id in [n.id for n in client.networks.list()]
        assert network.id not in [
            n.id for n in
            client.networks.list(ids=["fdhjklfdfdshjkfds"])
        ]
        assert network.id in [
            n.id for n in
            client.networks.list(ids=[network.id])
        ]
        assert network.id not in [
            n.id for n in
            client.networks.list(names=["fdshjklfdsjhkl"])
        ]
        assert network.id in [
            n.id for n in
            client.networks.list(names=[name])
        ]
        network.remove()
        assert network.id not in [n.id for n in client.networks.list()]


class ImageTest(BaseIntegrationTest):

    def test_connect_disconnect(self):
        client = docker.from_env()
        network = client.networks.create(helpers.random_name())
        self.tmp_networks.append(network.id)
        container = client.containers.create("alpine", "sleep 300")
        self.tmp_containers.append(container.id)
        assert network.containers == []
        network.connect(container)
        container.start()
        assert client.networks.get(network.id).containers == [container]
        network.disconnect(container)
        assert network.containers == []
        assert client.networks.get(network.id).containers == []
