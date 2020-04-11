#!/usr/bin/env python
#coding:utf8
from fabric.colors import *
from fabric.api import *
import os
import sys
import hashlib
import datetime
import re
import json

with open('mtj_game.json','r') as f:
    games_list = json.load(f)
print(games_list)

hosts = []
games = []
server_list = open("gameserver_id.txt")
lines = server_list.readlines()          #读取游戏服列表
for line in lines:
    data = line.strip()
    if len(data) != 0:
        if data not in games:
            games.append(data)                  #游戏服列表，例如game1、game2
        if games_list[data] not in hosts:
            hosts.append(games_list[data])

print ("更新的服务器ip：%s" %hosts)
print ("更新的游戏服id：%s" %games)

env.hosts=hosts
env.user = 'root'
env.port = 8622

#本地目录
work_dir='/mydata/mtj/'
#远程服服目录
remote_dir='/data/mtj'


@task
@parallel(pool_size=5)
def scp_gamejar():      ###拷贝jar包和config文件到 /data/mtj/下 ，以防更新失败
    with lcd(work_dir):
        conf_file="mtj_config.tar.gz"
        jarfile="mtj_game-all.jar"
        put(jarfile,remote_dir)
        print(green("jar文件传输完成！"))
        put(conf_file,remote_dir)
        print(green("config文件传输完成！"))

#@task
#def mysql_del_data():      ###数据库清档（清除表数据）
#    with cd(remote_dir):
#        output = run("ls | grep 'mtj_[0-9]\{1,8\}$'")
#        youxifu_list = (output.strip()).split("\n")
#        for youxifu in youxifu_list:
#            youxifu=youxifu.replace("\r","")
#            import_sql = "mysql -uroot -p8Blfhxz5SxfswsScqdb " + youxifu + " < /tmp/mtj_game1_d.sql"
#            run(import_sql)

@task
@parallel
def kill_pid():         #kill  游戏进程
    with cd(remote_dir):
        output = run("ls | grep 'mtj_[0-9]\{1,8\}$'")
        youxifu_list = (output.strip()).split("\n")
        for youxifu in youxifu_list:
            for qufu in iter(games):
                if youxifu.replace("\r","").split("_")[1] == qufu.replace("game",""):
                    qufu=qufu.replace("game","")
                    with cd("mtj_" + qufu + "/work/"):
                        stdout = run("kill -9 `cat server.pid`")
                        if "" == str(stdout).strip():
                            print(green("游戏%s区停服成功" % qufu))
                        else:
                            print (red("游戏%s区停服失败" % qufu))

@task
@runs_once
def pull_code():
    global model ,value ,local_config_time ,local_game_md5
    model = prompt('请输入模块名首字母:{a(admin),c(config),g(game),m(master)}', default='gc', validate=str)
    value = prompt('是否执行startup.sh:(y/n)', default='y', validate=str)

@task
@parallel(pool_size=5)
def transfer():                 #ftp传输文件game、config
    with lcd(work_dir):
        if 'c' in model:
            with cd(remote_dir):
                print (green("开始备份mtj_config.tar.gz"))
                back_file = "\cp mtj_config.tar.gz /tmp/"
                run(back_file)
            local_file = "mtj_config.tar.gz"
            print (green("开始传输mtj_config.tar.gz文件..."))
            put(local_file,remote_dir)
        for file in model:
            if file == 'g':
                file = 'game'
                with cd(remote_dir):
                    print (green("开始备份mtj_game-all.jar"))
                    back_file = "\cp mtj_game-all.jar /tmp/"
                    run(back_file)
                print (green("开始传输mtj_" + file + "-all.jar文件..."))
                local_file = "mtj_" + file + "-all.jar"                     #mtj_game-all.jar
                put(local_file, remote_dir)
@task
@parallel(pool_size=2)
def depress():  # 只解压,移动
    with cd(remote_dir):
        output = run("ls | grep 'mtj_[0-9]\{1,8\}$'")
        youxifu_list = (output.strip()).split("\n")

        if 'c' in model:
            print (yellow("开始解压mtj_config.tar.gz文件"))
            unzip_file = "tar xf mtj_config.tar.gz"
            run(unzip_file)

        for line in model:
            if line == 'g':
                line = 'game'
                for youxifu in youxifu_list:
                    for qufu in iter(games):
                        if youxifu.replace("\r", "").split("_")[1] == qufu.replace("game",""):
                            qufu=qufu.replace("game","")
                            print (yellow("开始移动mtj_" + line + "-all.jar文件到mtj_" + qufu + "/lib/目录下"))
                            cp_file = "\cp mtj_game-all.jar mtj_" + qufu + "/lib/"
                            run(cp_file)

@task
def exec_startup():         #执行startup.sh 脚本
    with cd(remote_dir):
        output = run("ls | grep 'mtj_[0-9]\{1,8\}$'")
        youxifu_list = (output.strip()).split("\n")

        if 'c' in model:
            if model == 'c':
                if value in ["Y", "y"]:
                    for youxifu in youxifu_list:
                        for qufu in iter(games):
                            if youxifu.replace("\r", "").split("_")[1] == qufu.replace("game",""):
                                print (qufu)
                                qufu=qufu.replace("game","")
                                with cd('mtj_' + qufu):
                                    run('sh startup.sh',
                                        pty=False)  # pty参数作用，执行完此命令，是否杀死改进程。默认为True，表示杀死
                                    new_jps = run('pgrep java')
                                    with cd("work/"):
                                        stdout = run("cat server.pid")
                                        if str(stdout).strip() in str(new_jps).strip():
                                            print (green("游戏%s区启动成功" % qufu))
                                        else:
                                            print (red("游戏%s区启动失败" % qufu))
                                    run('ls -ld ../mtj_config')
                                    # sys.exit(0)                不能使用这个，直接退出程序导致后面一台机器没有执行此脚本

        for line in model:
            if line == 'g':
                line = 'game'
                for youxifu in youxifu_list:
                    for qufu in iter(games):
                        if youxifu.replace("\r", "").split("_")[1] == qufu.replace("game",""):
                            qufu=qufu.replace("game","")
                            if value in ['Y', 'y']:
                                #print green("原始进程号")
                                #run('jps')
                                print ("开始执行" + qufu + "目录下的startup.sh")
                                with cd('mtj_' + qufu + "/"):
                                    run('sh startup.sh', pty=False)
                                    new_jps = run('pgrep java')
                                    with cd("work/"):
                                        stdout = run("cat server.pid")
                                        if str(stdout).strip() in str(new_jps).strip():
                                            print (green("游戏%s区启动成功" % qufu))
                                        else:
                                            print (red("游戏%s区启动失败" % qufu))
                                    run('ls -l lib/mtj_' + line + '-all.jar')

@task
@parallel(pool_size=2)
def rollback():                     #进行回滚操作
    with cd(remote_dir):
        output = run ("ls | grep 'mtj_[0-9]\{1,8\}$'")
        youxifu_list = (output.strip()).split("\n")
        if 'c' in model:
            print(yellow("开始回滚mtj_config.tar.gz文件"))
            rollback_file = "\cp /tmp/mtj_config.tar.gz . && tar xf mtj_config.tar.gz"
            run(rollback_file)
            run('ls -l mtj_config.tar.gz')
            print(green("mtj_config回滚成功"))

        for line in model:
            if line == 'g':
                line = 'game'
                for  youxifu in youxifu_list:
                    for qufu in iter(games):
                        if youxifu.replace("\r","").split("_")[1] == qufu.replace("game",""):
                            qufu=qufu.replace("game","")
                            print(yellow("开始回滚mtj_" +line +"-all.jar文件到mtj_"+qufu +"/lib/目录下"))
                            rollback_file = "\cp /tmp/mtj_game-all.jar . && cp /tmp/mtj_game-all.jar  mtj_" + qufu + "/lib/"
                            run(rollback_file)
                            run('ls -l mtj_'+qufu +'/lib/mtj_'+ line + '-all.jar')
                            print(green("游戏%s服回滚成功"  % qufu))

@task
def see_jps():                  #使用命令jps查看游戏进程是否正在运行
    with cd(remote_dir):
        output = run("ls | grep 'mtj_[0-9]\{1,8\}$'")
        youxifu_list = (output.strip()).split("\n")

    for youxifu in youxifu_list:
        for qufu in iter(games):
            if youxifu.replace("\r", "").split("_")[1] == qufu.replace("game",""):
                qufu=qufu.replace("game","")
                with cd(remote_dir):
                    with cd('mtj_' + qufu + "/"):
                        with cd("work/"):
                            new_jps = run('jps')
                            stdout = run("cat server.pid")
                            if str(stdout).strip() in str(new_jps).strip():
                                print (green("游戏%s区正在运行" % qufu))
                                print ("******************************************")
                            else:
                                print (red("游戏%s区停止运行" % qufu))
                                print ("******************************************")