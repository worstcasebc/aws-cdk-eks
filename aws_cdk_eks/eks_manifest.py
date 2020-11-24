from aws_cdk import core, aws_eks, aws_ec2


class EKSManifest(core.Construct):

    def __init__(self, scope: core.Construct, id: str, cluster, manifest, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.cluster = cluster
        self.manifest = manifest
        
        def backend_service(self, manifest):
            labels = manifest['labels']
            deployment = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {"name": manifest['service_name'], "namespace": "default"},
                "spec": {
                    "replicas": manifest['replicas'],
                    "selector": {"matchLabels": labels},
                    "strategy": {
                      "rollingUpdate": {
                          "maxSurge": "25%",
                          "maxUnavailable": "25%"
                      }
                    },
                    "template": {
                        "metadata": {"labels": labels},
                        "spec": {
                            "containers": [{
                                "name":  manifest['service_name'],
                                "image": manifest['image'],
                                "ports": [{"containerPort": manifest['port'], "protocol": "TCP"}]
                            }
                            ]
                        }
                    }
                }
            }
            
            service = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {"name": manifest['service_name'], "namespace": "default"},
                "spec": {
                    "type": "LoadBalancer",
                    "ports": [{"port": 80, "targetPort": manifest['port']}],
                    "selector": manifest['labels']
                }
            }
            
            return deployment, service
        
        def frontend_service(self, manifest):
            labels = manifest['labels']
            deployment = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {"name": manifest['service_name'], "namespace": "default"},
                "spec": {
                    "replicas": manifest['replicas'],
                    "selector": {"matchLabels": labels},
                    "strategy": {
                      "rollingUpdate": {
                          "maxSurge": "25%",
                          "maxUnavailable": "25%"
                      }
                    },
                    "template": {
                        "metadata": {"labels": labels},
                        "spec": {
                            "containers": [{
                                "name":  manifest['service_name'],
                                "image": manifest['image'],
                                "ports": [{"containerPort": manifest['port'], "protocol": "TCP"}],
                                "env": manifest['env'] 
                            }
                            ],
                        }
                    }
                }
            }
            
            service = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {"name": manifest['service_name'], "namespace": "default"},
                "spec": {
                    #"type": "ClusterIP",
                    "ports": [{"port": 80, "targetPort": manifest['port'], "protocol": "TCP"}],
                    "selector": manifest['labels']
                }
            }
            
            return deployment, service
        
        fargate_eks_ALB_ingress_manifest = {
            "apiVersion": "extensions/v1beta1",
            "kind": "Ingress",
            "metadata": {
                "name": "fargate-eks-alb-ingress",
                "namespace": "default",
                "annotations": {
                    "kubernetes.io/ingress.class": "alb",
                    "alb.ingress.kubernetes.io/scheme": "internet-facing",
                    "alb.ingress.kubernetes.io/target-type": "ip",
                    #"alb.ingress.kubernetes.io/listen-ports": "[{"HTTP": 80}, {"HTTP":5000}]"
                },
                "labels": manifest['labels'],
            },
            "spec": {
                "rules": [{
                    "http": {
                        "paths": [{
                            "path": "/*",
                            "backend": {
                                "serviceName": "flask",
                                "servicePort": 80
                            },
                        }],
                    },
                }],
            },
        }
        
        if self.manifest['service_type'] == 'backend':
            deployment_manifest, service_manifest = backend_service(self, self.manifest)
        elif self.manifest['service_type'] == 'frontend':
            deployment_manifest, service_manifest = frontend_service(self, self.manifest)
        
        aws_eks.KubernetesManifest(self, "DeploymentServiceManifest", cluster=self.cluster, manifest=[deployment_manifest, service_manifest, fargate_eks_ALB_ingress_manifest])