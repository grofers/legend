import kopf


@kopf.on.login()
def login_handler(**kwargs):
    """
    Implements a login handler to make Kopf work outside of a Kubernetes
    cluster. Doesn't work without having a proxy connection opened with the
    Kubernetes cluster using `kubectl proxy`.
    """

    return kopf.ConnectionInfo(
        server="http://localhost:8001",
        insecure=True,
    )
