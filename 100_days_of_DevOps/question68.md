```
The DevOps team at xFusionCorp Industries is initiating the setup of CI/CD pipelines and has decided to utilize Jenkins as their server. Execute the task according to the provided requirements:



1. Install Jenkins on the jenkins server using the apt utility only, and start it using the service command. The jenkins server runs Ubuntu without systemd (systemctl does not work there), and current Jenkins releases need Java 21 or later (for example openjdk-21-jre).

If you face a timeout issue while starting the Jenkins service, first check the service status with service jenkins status
Then review the logs in /var/log/jenkins/jenkins.log to identify the cause.
2. Jenkin's admin user name should be theadmin, password should be Adm!n321, full name should be Javed and email should be javed@jenkins.stratos.xfusioncorp.com.


Note:

1. To access the jenkins server, connect from the jump host using the root user with the password S3curePass (if it is refused right after the lab starts, wait a minute: the server is still being prepared).

2. After Jenkins server installation, click the Jenkins button on the top bar to access the Jenkins UI and follow on-screen instructions to create an admin user.


----------------------------------------------

You'll need to SSH from the jump host into the Jenkins server, install Java 21 and Jenkins using apt, and start Jenkins using service (not systemctl).

Here is the step-by-step command sequence for this lab.
1. Connect to the Jenkins server
From the jump host, run:
ssh root@jenkins


When prompted for the password, enter:
S3curePass


If SSH is initially refused, wait about a minute and retry.
2. Install Java 21
On the Jenkins server, run:
apt update
apt install -y fontconfig openjdk-21-jre


Verify Java:
java -version


Jenkins requires Java 21 or newer for current releases. 
Jenkins

3. Add the Jenkins repository
Run the following as root:
mkdir -p /etc/apt/keyrings

wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" > /etc/apt/sources.list.d/jenkins.list

apt update


4. Install Jenkins
apt install -y jenkins


5. Start Jenkins using service
Do not use systemctl in this lab.
service jenkins start


Check status:
service jenkins status


If it takes time or fails to start:
service jenkins status
cat /var/log/jenkins/jenkins.log


6. Unlock Jenkins
On the Jenkins server, retrieve the initial administrator password:
cat /var/lib/jenkins/secrets/initialAdminPassword


Copy the password displayed.
7. Configure the Jenkins UI
Click the Jenkins button on the top bar of the lab and follow the setup wizard.
1. Paste the initial administrator password.
2. Select Install suggested plugins (if prompted).
3. On the Create First Admin User page, enter:
Field	Value
Username	theadmin
Password	Adm!n321
Confirm password	Adm!n321
Full name	Javed
Email	javed@jenkins.stratos.xfusioncorp.com

4. Click Save and Continue.
5. Complete the remaining setup and click Start using Jenkins.
The task is complete once Jenkins is running and the specified admin user has been created.

These commands follow the current Jenkins Debian installation procedure using the LTS repository and apt. 
Jenkins

