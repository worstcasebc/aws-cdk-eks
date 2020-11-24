from aws_cdk import core, aws_ec2

class EKSVpc(core.Construct):
    
    def __init__(self, scope: core.Construct, id: str, vpc_nat_gateways, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.vpc_nat_gateways = vpc_nat_gateways 
        self.vpc = None
        
        if self.vpc_nat_gateways == None:
            self.vpc = aws_ec2.Vpc(self, "ClusterVPC", 
                cidr="10.0.0.0/16"
            )
        else:
            self.vpc = aws_ec2.Vpc(self, "ClusterVPC",
                cidr="10.0.0.0/16", 
                nat_gateways=self.vpc_nat_gateways,
            )