# secret-kitty
A keys from the bowl game

## Requirements
* [Docker for Mac](https://www.docker.com/docker-mac)

## Usage
* Build and run container

```
$ make build
$ make up
```

* Get winner

#### plaintext

```
$ make get-winner
# or
$ curl http://127.0.0.1:3000
Frances
```

#### json

```
$ make get-winner-json
# or
$ curl http://127.0.0.1:3000/json
{
  "name": "Frances"
}
```

### Helm chart
NOTE depends on [nginx-ingress](https://github.com/kubernetes/charts/tree/master/stable/nginx-ingress), [external-dns](https://github.com/kubernetes/charts/tree/master/stable/external-dns), and [kube-lego](https://github.com/kubernetes/charts/tree/master/stable/kube-lego)

#### Deploy

```bash
$ make deploy
```

#### Delete

```bash
$ make delete
```
