# SNP encrypted storage demo

_Note: this is a dump of notes I have for a demo and I wrote them a while ago, so it's not really tested_

This demo showcases how to decrypt a big blog that's encrypted by columns within a Confindential Container.

## Build

```
pip install -r requirements.txt
```

## Generate CSV

```
python3 gen_csv.py
```

## Encrypt

```
python3 encrypt.py
```

## Upload encryption key to KBS

```
KBS_POD=$(kubectl get pod -l app=kbs -o jsonpath="{.items[0].metadata.name}")
kubectl exec "$KBS_POD" -it -- mkdir -p /opt/confidential-containers/kbs/repository/default/key/
kubectl cp df_enc.key "$KBS_POD":/opt/confidential-containers/kbs/repository/default/key/secretkey
```

## Deploy

```
demo_image="ghcr.io/${my_org}/snp-demo:r1"
docker build -t "$demo_image" .
docker push "$demo_image"
cat <<EOF > ./snp-demo.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: snp-demo
spec:
  template:
    spec:
      runtimeClassName: kata-remote
      serviceAccountName: csi-azurefile-podvm-sa
      containers:
      - name: csi-podvm-wrapper
        env:
          - name: POD_NAME
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
          - name: POD_NAME_SPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
          - name: POD_UID
            valueFrom:
              fieldRef:
                fieldPath: metadata.uid
          - name: POD_NODE_NAME
            valueFrom:
              fieldRef:
                fieldPath: spec.nodeName
        args:
          - -v=2
          - --endpoint=/tmp/csi-podvm-wrapper.sock
          - --target-endpoint=/tmp/csi.sock
          - --namespace=kube-system
        image: quay.io/confidential-containers/csi-podvm-wrapper:latest
        imagePullPolicy: Always
        volumeMounts:
          - mountPath: /tmp
            name: plugin-dir
      - name: snp-demo
        image: $demo_image
        imagePullPolicy: Always
        volumeMounts:
        - name: encrypted-data
          mountPath: /mnt
        env:
        - name: DESCRIPTION
          value: "she found her glasses while they were looking somewhere else"
        resources:
          requests:
            memory: "128Mi"
            cpu: "1000m"
          limits:
            memory: "300Mi"
            cpu: "1000m"
      volumes:
        - emptyDir: {}
          name: plugin-dir
        - name: encrypted-data
          persistentVolumeClaim:
            claimName: pvc-azurefile
      restartPolicy: Never
EOF
kubectl apply -f ./snp-demo.yaml
```
