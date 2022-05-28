# todo

####Job1 - check relays - relayread-redis
####Read relay state
####Write relay state to relay/type/state

#Job2 - thermo calendar
#Read thermo calendar from radicale - populate redis
#Read water calendar - populate redis

#Job3 - water
#Read redis for water
#Read user override for water user/water/requested
#Determine if boiler should be on
#Write requested state to relay/water/requestedstate

Job 4
Move ingress to it's own namespace to speak to the services inside the other namespaces

Job 5 - thermostat
Read thermo from redis
Read temperatures from redis (calendar and user/heat/requested)
Determine if boiler should be on
Write requested state to relay/heat/requestedstate

Job6 - update relays
Compare relay/type/state to relay/type/requested. Adjust if different.
Write relay state to relay/type/state

Pruning
docker system prune -a

root@hotfsd:~/hotfv3/monitoring/linux-arm64# export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
root@hotfsd:~/hotfv3/monitoring/linux-arm64# helm install --generate-name prometheus-community/prometheus
NAME: prometheus-1653149599
LAST DEPLOYED: Sat May 21 17:13:55 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-1653149599-server.default.svc.cluster.local


Get the Prometheus server URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace default -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace default port-forward $POD_NAME 9090


The Prometheus alertmanager can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-1653149599-alertmanager.default.svc.cluster.local


Get the Alertmanager URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace default -l "app=prometheus,component=alertmanager" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace default port-forward $POD_NAME 9093
#################################################################################
######   WARNING: Pod Security Policy has been moved to a global property.  #####
######            use .Values.podSecurityPolicy.enabled with pod-based      #####
######            annotations                                               #####
######            (e.g. .Values.nodeExporter.podSecurityPolicy.annotations) #####
#################################################################################


The Prometheus PushGateway can be accessed via port 9091 on the following DNS name from within your cluster:
prometheus-1653149599-pushgateway.default.svc.cluster.local


Get the PushGateway URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace default -l "app=prometheus,component=pushgateway" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace default port-forward $POD_NAME 9091

For more information on running Prometheus, visit:
https://prometheus.io/

