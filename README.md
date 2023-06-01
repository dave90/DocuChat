# DocuChat

You can find the full explanation of the repository:  [From messy notebook code to clean kubernetes pods](https://dave90.github.io/posts/docu-chat-2/)

## Structure of repository

- Agent: The Agent service manage the queries with the LLM model.
- DBVector: Manages the storing and retrieving data to vector DB.
- TextToVector: service that manage the storing of chunks of text. It takes a long text and it split in chunks and store the chunks into the DB Vector calling the DB Vector service.
- docuchat: Helm chart definition
  - values.yml: defines the all parameters
  - templates/deployment.yaml: defines the pods
  - templates/service.yaml: defines the services
  - templates/ingress.yaml: defines the ingress rules
  - templates/pvc.yaml: defines the persistence volume claim

- UI: simple chat that will allow to talk with the bot.

## Helm

### Install Nginx ingress to aks

- NAMESPACE=docuchat
- helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
- helm repo update
- helm install ingress-nginx ingress-nginx/ingress-nginx \
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

### DocuChat UI

TODO