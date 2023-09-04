for CRD in `ls -1 crd/*.yml`; do
    echo "Creating CRD: ${CRD}"
    kubectl apply -f ${CRD}
done