from aws_cdk import core, aws_eks, aws_ec2
from .eks_vpc import EKSVpc
from .eks_base import EKSBase
from .eks_manifest import EKSManifest
from .alb_ingress import ALBIngressController


class AwsCdkEksStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, 
    eks_version=aws_eks.KubernetesVersion.V1_18, cluster_name=None, vpc_nat_gateways=None, 
    capacity_details='small', fargate_enabled=False, frontend_service={}, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.eks_version = eks_version
        self.cluster_name = cluster_name
        self.vpc_nat_gateways = vpc_nat_gateways
        self.capacity_details = capacity_details
        self.fargate_enabled = fargate_enabled
        self.frontend_service = frontend_service
        # 
        config_dict = {
            'eks_version': self.eks_version,
            'cluster_name': self.cluster_name,
            'capacity_details': self.capacity_details,
            'fargate_enabled': self.fargate_enabled,
        }
        
        base_vpc = EKSVpc(self, "ClusterVPC", 
            vpc_nat_gateways=self.vpc_nat_gateways
        )
        base_cluster = EKSBase(self, "Base", 
            cluster_vpc=base_vpc, 
            cluster_configuration=config_dict
        )
        alb_ingress = ALBIngressController(self, "ALBIngress", 
            cluster=base_cluster.cluster
        )
        frontend_service = EKSManifest(self, "FrontendService", 
            cluster=base_cluster.cluster, 
            manifest=self.frontend_service
        )
        