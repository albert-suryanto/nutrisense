# nutrisense

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.16.0](https://img.shields.io/badge/AppVersion-1.16.0-informational?style=flat-square)

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| app.livenessProbe.httpGet.path | string | `"/"` |  |
| app.livenessProbe.httpGet.port | string | `"http"` |  |
| app.livenessProbe.initialDelaySeconds | int | `10` |  |
| app.logger.level | string | `"debug"` |  |
| app.readinessProbe.httpGet.path | string | `"/"` |  |
| app.readinessProbe.httpGet.port | string | `"http"` |  |
| app.readinessProbe.initialDelaySeconds | int | `10` |  |
| app.server.env | string | `"development"` |  |
| app.server.host | string | `"0::0"` |  |
| app.server.port | int | `8000` |  |
| app.server.ttl | string | `"20s"` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| autoscaling.targetMemoryUtilizationPercentage | int | `80` |  |
| cronjobs | list | `[]` |  |
| deploy | bool | `true` |  |
| envFile.deploy | bool | `true` |  |
| envFile.key | string | `".env"` |  |
| envFile.name | string | `"envfile"` |  |
| externalSecret.policy.creation | string | `"Owner"` |  |
| externalSecret.policy.deletion | string | `"Retain"` |  |
| externalSecret.remoteRef.key | string | `""` |  |
| externalSecret.secretStore.kind | string | `"ClusterSecretStore"` |  |
| externalSecret.secretStore.name | string | `"awsssm-store"` |  |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"nutrisense"` |  |
| image.tag | string | `""` |  |
| imagePullSecrets[0].name | string | `"team-rbac-setup-docker-pull-secret-team"` |  |
| ingress.annotations | object | `{}` |  |
| ingress.className | string | `"traefik"` |  |
| ingress.enabled | bool | `true` |  |
| ingress.hosts[0].host | string | `"api.nutrisense.127.0.0.1.nip.io"` |  |
| ingress.hosts[0].paths[0].path | string | `"/"` |  |
| ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| ingress.tls | list | `[]` |  |
| nameOverride | string | `""` |  |
| nodeSelector."kubernetes.io/arch" | string | `"arm64"` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources.limits.cpu | int | `1` |  |
| resources.limits.memory | string | `"2Gi"` |  |
| resources.requests.cpu | float | `0.5` |  |
| resources.requests.memory | string | `"1Gi"` |  |
| securityContext.allowPrivilegeEscalation | bool | `false` |  |
| securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| securityContext.privileged | bool | `false` |  |
| securityContext.readOnlyRootFilesystem | bool | `false` |  |
| securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| service.port | int | `80` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `false` |  |
| serviceAccount.name | string | `"nutrisense-service-account"` |  |
| tolerations | list | `[]` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.2](https://github.com/norwoodj/helm-docs/releases/v1.11.2)
