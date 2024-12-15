# Homework 10: Notes

Clone the repository and change dir to the homework-10 folder

```bash
git clone https://github.com/jdanussi/ml-zoomcamp-2024.git
cd ml-zommcamp-2024/homework-10
```

Build the docker image for the subsciption service and run the container
```bash
docker build -t zoomcamp-model:3.11.5-hw10 .
docker run -it --rm -p 9696:9696 zoomcamp-model:3.11.5-hw10
INFO:waitress:Serving on http://0.0.0.0:9696
```

Test the prediction service from another terminal
```bash
python q6_test.py
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
```

In my case, I already have `kubectl` and `kind` installed
```bash
kubectl version
Client Version: v1.31.1
Kustomize Version: v5.4.2
Server Version: v1.28.0
WARNING: version difference between client (1.31) and server (1.28) exceeds the supported minor version skew of +/-1

kind --version
kind version 0.20.0

# Cluster details
kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:46163
CoreDNS is running at https://127.0.0.1:46163/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

# Type of the service that is already running
kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   319d

# Load the service image into kind cluster
kind load docker-image zoomcamp-model:3.11.5-hw10
Image: "zoomcamp-model:3.11.5-hw10" with ID "sha256:86e80575d98977ea2a621b489cea1cb0fdcd1aa61293165d504e0c3ac63d514f" not yet present on node "kind-control-plane", loading...
Image: "zoomcamp-model:3.11.5-hw10" with ID "sha256:86e80575d98977ea2a621b489cea1cb0fdcd1aa61293165d504e0c3ac63d514f" not yet present on node "kind-worker2", loading...
Image: "zoomcamp-model:3.11.5-hw10" with ID "sha256:86e80575d98977ea2a621b489cea1cb0fdcd1aa61293165d504e0c3ac63d514f" not yet present on node "kind-worker3", loading...
Image: "zoomcamp-model:3.11.5-hw10" with ID "sha256:86e80575d98977ea2a621b489cea1cb0fdcd1aa61293165d504e0c3ac63d514f" not yet present on node "kind-worker", loading...
```

Deploying resource into the kind cluster
```bash
kubectl apply -f deployment.yaml 
deployment.apps/subscription created

kubectl get pods
NAME                           READY   STATUS    RESTARTS   AGE
subscription-6d55c5fb6-hh2l2   1/1     Running   0          11s


kubectl apply -f service.yaml 
service/subscription created

kubectl get svc
NAME           TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes     ClusterIP      10.96.0.1      <none>        443/TCP        319d
subscription   LoadBalancer   10.96.180.36   <pending>     80:32549/TCP   7s
```

Testing the service from kubernetes
```bash
kubectl port-forward service/subscription 9696:80
Forwarding from 127.0.0.1:9696 -> 9696
Forwarding from [::1]:9696 -> 9696
Handling connection for 9696

# From another terminal we run the test
python q6_test.py
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
```

## HPA

create the HPA 
```bash
kubectl autoscale deployment subscription --name subscription-hpa --cpu-percent=20 --min=1 --max=3=3
horizontalpodautoscaler.autoscaling/subscription-hpa autoscaled
```

Check the current status of the new HPA 
```bash
kubectl get hpa
NAME               REFERENCE                 TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
subscription-hpa   Deployment/subscription   <unknown>/20%   1         3         1          21s
```

The TARGETS column doesn't show pod metrics. We installed the Metrics Server.
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
serviceaccount/metrics-server created
clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader created
clusterrole.rbac.authorization.k8s.io/system:metrics-server created
rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader created
clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator created
clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server created
service/metrics-server created
deployment.apps/metrics-server created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io created
```

Since the problem is not solved, we checked the logs of the Metrics Server.
```bash
kubectl logs -n kube-system deployment/metrics-server

I1214 23:20:30.845361       1 server.go:191] "Failed probe" probe="metric-storage-ready" err="no metrics to serve"
E1214 23:20:32.460710       1 scraper.go:149] "Failed to scrape node" err="Get \"https://172.21.0.5:10250/metrics/resource\": tls: failed to verify certificate: x509: cannot validate certificate for 172.21.0.5 because it doesn't contain any IP SANs" node="kind-control-plane"
E1214 23:20:32.465782       1 scraper.go:149] "Failed to scrape node" err="Get \"https://172.21.0.2:10250/metrics/resource\": tls: failed to verify certificate: x509: cannot validate certificate for 172.21.0.2 because it doesn't contain any IP SANs" node="kind-worker"
E1214 23:20:32.491150       1 scraper.go:149] "Failed to scrape node" err="Get \"https://172.21.0.4:10250/metrics/resource\": tls: failed to verify certificate: x509: cannot validate certificate for 172.21.0.4 because it doesn't contain any IP SANs" node="kind-worker3"
E1214 23:20:32.491938       1 scraper.go:149] "Failed to scrape node" err="Get \"https://172.21.0.3:10250/metrics/resource\": tls: failed to verify certificate: x509: cannot validate certificate for 172.21.0.3 because it doesn't contain any IP SANs" node="kind-worker2"
```
 
There are problems with SSL certificates. As We are not working in a production environment We can setup Metrics Server without SSL certificates.

Edit the Metrics Server Deployment:
```bash
kubectl edit deployment metrics-server -n kube-system
```
Add the following argument to the spec.containers.args section:
```yaml
- --kubelet-insecure-tls
- --kubelet-preferred-address-types=InternalIP
```

Now We check the Metrics Server is running correctly (collecting the metrics)
```bash
kubectl top pods
NAME                           CPU(cores)   MEMORY(bytes)   
subscription-6d55c5fb6-hh2l2   36m          92Mi            

kubectl top nodes
NAME                 CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
kind-control-plane   325m         4%     908Mi           2%        
kind-worker          355m         4%     560Mi           1%        
kind-worker2         249m         3%     507Mi           1%        
kind-worker3         272m         3%     459Mi           1%        

# We run the test in an infinity loop to stress the service 
python q6_test_stress.py 
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
{'has_subscribed': True, 'has_subscribed_probability': 0.756743795240796}
...

# Check the hpa's reaction to the increased service demand.
kubectl get hpa subscription-hpa --watch
NAME               REFERENCE                 TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
subscription-hpa   Deployment/subscription   18%/20%   1         3         2          39m
subscription-hpa   Deployment/subscription   17%/20%   1         3         2          39m
subscription-hpa   Deployment/subscription   19%/20%   1         3         2          40m
subscription-hpa   Deployment/subscription   17%/20%   1         3         2          40m
subscription-hpa   Deployment/subscription   18%/20%   1         3         2          41m
subscription-hpa   Deployment/subscription   15%/20%   1         3         2          41m
subscription-hpa   Deployment/subscription   18%/20%   1         3         2          42m
subscription-hpa   Deployment/subscription   17%/20%   1         3         2          42m
subscription-hpa   Deployment/subscription   18%/20%   1         3         2          43m
subscription-hpa   Deployment/subscription   17%/20%   1         3         2          44m
subscription-hpa   Deployment/subscription   18%/20%   1         3         2          44m
subscription-hpa   Deployment/subscription   17%/20%   1         3         2          45m
subscription-hpa   Deployment/subscription   18%/20%   1         3         2          46m
subscription-hpa   Deployment/subscription   17%/20%   1         3         2          46m
```
