from aws_cdk import core, aws_eks, aws_ec2


class EKSBase(core.Construct):

    def __init__(self, 
        scope: core.Construct, 
        id: str, 
        cluster_vpc, 
        cluster_configuration, 
        **kwargs
        ) -> None:
        
        super().__init__(scope, id, **kwargs)
        self.cluster_vpc = cluster_vpc
        self.cluster_configuration = cluster_configuration  
        
        def determine_cluster_size(self):
            """
            return instance_size, node_count
            """
            if self.cluster_configuration['capacity_details'] == 'small':
                # default to fargate only
                instance_details = aws_ec2.InstanceType.of(aws_ec2.InstanceClass.BURSTABLE2, aws_ec2.InstanceSize.MICRO)
                instance_count = 3
            elif self.cluster_configuration['capacity_details'] == 'medium':
                instance_details = aws_ec2.InstanceType.of(aws_ec2.InstanceClass.COMPUTE5, aws_ec2.InstanceSize.MEDIUM)
                instance_count = 3
            elif self.cluster_configuration['capacity_details'] == 'large':
                instance_details = aws_ec2.InstanceType.of(aws_ec2.InstanceClass.COMPUTE5, aws_ec2.InstanceSize.LARGE)
                instance_count = 6
            else:
                # For a non specified capacity cluster, we will default to zero nodes and fargate only
                instance_count = 0
                instance_details = aws_ec2.InstanceType.of(aws_ec2.InstanceClass.BURSTABLE2, aws_ec2.InstanceSize.MICRO)
                self.cluster_configuration['fargate_enabled'] == True
            
            return { 'default_capacity': instance_count, 'default_capacity_instance': instance_details }
         
        capacity_details = determine_cluster_size(self)
                
        if self.cluster_configuration['fargate_enabled'] is True:
            # Create a FargateCluster without Instance-nodes
            self.cluster = aws_eks.FargateCluster(
                self, "EKSCluster",
                version = self.cluster_configuration['eks_version'],
                cluster_name = self.cluster_configuration['cluster_name'],
                vpc = self.cluster_vpc.vpc,
                vpc_subnets = [
                    aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE), 
                    aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC)
                ]
            )
        else:
            # Create an EKS cluster with default nodegroup configuration     
            self.cluster = aws_eks.Cluster(
                self, "EKSCluster",
                version = self.cluster_configuration['eks_version'],
                cluster_name = self.cluster_configuration['cluster_name'],
                vpc = self.cluster_vpc.vpc,
                vpc_subnets = [
                    aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE), 
                    aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC)
                ]
                **capacity_details
            )
        