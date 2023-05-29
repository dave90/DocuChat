# DocuChat

TODO

## Structure of repository

TODO

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

After the installation of the chart one pod is created for each services (db-vec,agent,text-to-vec and redis-stack-server). And ingress rules are applied:

- http://<CLUSTER IP OR DOMAIN>/text-to-vec: for storing the text
- http://<CLUSTER IP OR DOMAIN>/agent: for query the documents

Also a persistence volume is created to allow the redis-stack-server to persist the data.

Uninstall:

- helm uninstall docuchat --namespace $NAMESPACE