# Role to provision Spark cluster in oshinko

The role isn't idempotent at the moment. (specifically Oshinko Web UI provisioning part)

Common variables:
* `spark_project` - namespace name where to provision the cluster

## Provisioning of Oshinko Web UI

Run the role to provision Oshinko Web UI and pass variable `oshinko_deploy=true`.
By default Oshinko Web UI will not be provisioned.

Only one Oshinko Web UI is needed per namespace, it can support multiple Spark clusters.

## Provisioning of a Spark cluster

Run the role to provision Spark cluster.

Variables:
* `oshinko_spark_cluster` - name of the spark cluster to provision
* `spark_workers` - number of workers to provision

The spark Web UI will be provisioned and exposed via route at
`{{ oshinko_spark_cluster }}-{{ spark_project }}.{{ cluster suffix }}`

## Deletion

Run the role, pass the variable `spark_deploy=false` to the role to get
the Spark cluster wiped completely

