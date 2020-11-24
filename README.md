
# Example for an AWS CDK deployment of a Kubernetes Cluster with Fargate

This is an example of a CDK deployment for a K8s-Cluster with fargate-profile, running a docker-container, showing the actual hostname and IP-address.

Before you begin check, whether AWS CLI & CDK are installed on your machine:

```
$ aws --version
$ cdk --version
```

If not installed, you need to install it with

```
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
$ npm install -g aws-cdk
```

After checking out that Git-repository on Linux or Mac activate the virtualenv like this:

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

It may be necessary to export your credentials before running cdk-commands (at least on a Cloud9-environment):

```
$ export AWS_DEFAULT_REGION=<aws-region>
$ export AWS_ACCESS_KEY_ID=<access-key-id>
$ export AWS_SECRET_ACCESS_KEY=<secret-access-key>
```

Now open app.py and configure the eks you plan to deploy.

Cluster name: If none, will autogenerate

`cluster_name = "HandsOnCluster"`

Capacity details: Cluster size of (small|medium|large) will be ignored, if fargate enabled

`capacity_details = None`

Fargate enabled: Create a fargate profile on the cluster

`fargate_enabled = True`

Number of NAT-Gateways for VPC (None|int); None => One NAT gateway/instance per Availability Zone

`vpc_nat_gateways = 1`

Image of the container to run

`container_image = "docker.io/worstcaseffm/flaskserver:v1"`

To deploy that example t your AWS account run the following cdk-commands:

```
$ cdk bootstrap
$ cdk diff
$ cdk deploy
```

You may need to confirm the deployment by typing 'y' when asked for.

The deployment takes arround 30 min and will output two commands to update your kubectl-config and retrieve the token. After the deployment wait some more minutes for the pods running an the load-balancer comes up. 

```
$ aws elbv2 describe-load-balancers | grep DNSName
```

Check for the container running with that DNSName in your browser.

To destroy the whole build use the following command and ensure, you first delete the loadbalancer and the targetgroup and the loadbalancers security-group manually by the CLI or Mnagement Console.

```
$ cdk destroy
```

To add additional dependencies, for example other CDK libraries, just add them to your `setup.py` file and rerun the `pip install -r requirements.txt` command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
