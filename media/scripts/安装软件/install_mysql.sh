#!/bin/bash
echo "---------------------------- 将静态文件发布到 188.188.1.142 ----------------------------"
ssh tomcat@188.188.1.142 "sh /home/tomcat/scripts/deploy_baipao_front.sh"
echo "---------------------------- 将静态文件发布到 188.188.1.143 ----------------------------"
ssh tomcat@188.188.1.143 "sh /home/tomcat/scripts/deploy_baipao_front.sh"
# echo "---------------------------- 将静态文件传到 188.188.1.133 ----------------------------"
# ssh devuser@188.188.1.133 "sh /home/devuser/scripts/deploy_baipao_front.sh"