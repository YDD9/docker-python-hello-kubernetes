https://github.com/kubernetes/kubeadm/issues/546

Except ca-config.json and `ca-csr.json` only exists in etcd0,
all below command run on all etcd0, etcd1 and etcd2.

```
mkdir -p /etc/kubernetes/pki/etcd
cd /etc/kubernetes/pki/etcd

# first time ssh connection needs a confirm 'yes'
scp root@192.168.0.45:/etc/kubernetes/pki/etcd/ca.pem .

scp root@192.168.0.45:/etc/kubernetes/pki/etcd/ca-key.pem .
scp root@192.168.0.45:/etc/kubernetes/pki/etcd/client.pem .
scp root@192.168.0.45:/etc/kubernetes/pki/etcd/client-key.pem .
scp root@192.168.0.45:/etc/kubernetes/pki/etcd/ca-config.json .
```
Where `192.168.0.45` corresponds to the public or private IPv4 of etcd0.


```
cd /etc/kubernetes/pki/etcd
cfssl print-defaults csr > config.json
 sed -i '0,/CN/{s/example\.net/'"$PEER_NAME"'/}' config.json
 sed -i 's/www\.example\.net/'"$PRIVATE_IP"'/' config.json
 sed -i 's/example\.net/'"$PUBLIC_IP"'/' config.json

 cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server config.json | cfssljson -bare server
 cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=peer config.json | cfssljson -bare peer
```
This will result in the following files: `peer.pem`, `peer-key.pem`, `server.pem`, `server-key.pem`.


Install etcd binaries like so
```
export ETCD_VERSION=v3.1.10
 curl -sSL https://github.com/coreos/etcd/releases/download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz | tar -xzv --strip-components=1 -C /usr/local/bin/
 rm -rf etcd-$ETCD_VERSION-linux-amd64*
```

Generate the environment file that systemd will use:
```
 touch /etc/etcd.env
 echo "PEER_NAME=$PEER_NAME" >> /etc/etcd.env
 echo "PRIVATE_IP=$PRIVATE_IP" >> /etc/etcd.env
```

Copy the systemd unit, make sure you replace <etcd0-ip-address>192.168.0.45, <etcd1-ip-address>192.168.0.47 and <etcd2-ip-address>192.168.0.48 with the appropriate IPv4 addresses.
```
[Unit]
 Description=etcd
 Documentation=https://github.com/coreos/etcd
 Conflicts=etcd.service
 Conflicts=etcd2.service

 [Service]
 EnvironmentFile=/etc/etcd.env
 Type=notify
 Restart=always
 RestartSec=5s
 LimitNOFILE=40000
 TimeoutStartSec=0

 ExecStart=/usr/local/bin/etcd --name ${PEER_NAME} \
     --data-dir /var/lib/etcd \
     --listen-client-urls https://${PRIVATE_IP}:2379 \
     --advertise-client-urls https://${PRIVATE_IP}:2379 \
     --listen-peer-urls https://${PRIVATE_IP}:2380 \
     --initial-advertise-peer-urls https://${PRIVATE_IP}:2380 \
     --cert-file=/etc/kubernetes/pki/etcd/server.pem \
     --key-file=/etc/kubernetes/pki/etcd/server-key.pem \
     --client-cert-auth \
     --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.pem \
     --peer-cert-file=/etc/kubernetes/pki/etcd/peer.pem \
     --peer-key-file=/etc/kubernetes/pki/etcd/peer-key.pem \
     --peer-client-cert-auth \
     --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.pem \
     --initial-cluster etcd0=https://192.168.0.45:2380,etcd1=https://192.168.0.47:2380,etcd2=https://192.168.0.48:2380 \
     --initial-cluster-token my-etcd-token \
     --initial-cluster-state new

 [Install]
 WantedBy=multi-user.target
```
