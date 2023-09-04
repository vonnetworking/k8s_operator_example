PID=$(ps -ef | grep kube | grep "svc/argocd-server 8881" | awk '{print $2}')
[[ ! -z "$PID" ]] && kill ${PID}

#Check for pods in pending state and wait if needed
ARGO_IS_PENDING=`kubectl get pods -n argocd | grep -v "NAME" | grep -v "Running" | wc -l`

while [ ${ARGO_IS_PENDING} -ne 0 ]; do
    ARGO_IS_PENDING=`kubectl get pods -n argocd | grep -v "NAME" | grep -v "Running" | wc -l`
    echo "Argo Pod is still pending...sleeping..."
    kubectl get pods -n argocd
    sleep 3
done
kubectl port-forward --address localhost,192.168.50.200 svc/argocd-server 8881:80 8882:443 -n argocd &
sleep 2