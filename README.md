# DocuChat

## Helm

### Install Nginx ingress to aks

-NAMESPACE=ingress-basic
-helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
-helm repo update

-helm install ingress-nginx ingress-nginx/ingress-nginx \
  --create-namespace \
  --namespace $NAMESPACE \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz

Now you have a nginx LoadBalancer running. You can find the exposed cluster IP *EXTERNAL-IP* with:

- kubectl get services -A 

### Add Open AI API token

- OPENAI_API_KEY=<YOUR OPENAI API TOKEN>
- kubectl create secret generic openai-token --from-literal=token=$OPENAI_API_KEY --namespace $NAMESPACE

Check the secrets:

- kubectl get secrets --namespace $NAMESPACE

### Install DocuChat chart

- helm upgrade --install -f docuchat/values.yaml docuchat ./docuchat --namespace $NAMESPACE

Uninstall:

- helm uninstall docuchat --namespace $NAMESPACE