# SrunClient

基于[简易版深澜命令行客户端](https://github.com/ice-tong/SrunClient)适配MicroPython，包含登录登出和查询在线信息功能。支持
ESP32/ESP32C3(已经过测试的)。

# how to use

1. 使用命令行客户端登录登出
   在`srun.py`中修改`srun_ip`为自己学校对应的深澜网关地址
    ``` python3
      if __name__ == "__main__":
          srun_client = SrunClient()  ->  srun_client = SrunClient( srun_ip='202.204.105.195' ) 
          show_commands()
          srun_client.show_online()
    ``` 
   然后运行srun.py
    ``` 
    [user@host SrunClient]$ python srun.py
    ############### Wellcome to Srun Client ###############
    [1]: show online information
    [2]: set username and passwd
    [3]: login
    [4]: logout
    [h]: show this messages
    [q]: quit
    #######################################################
    [SrunClient CUGB] ###*** NOT ONLINE! ***###
    >
    ```

2. 掉线自动重连
    - 🍬**推荐**🍬 在 `main.py` 或 `boot.py` 中:
    ```
    # !!!注意: 在此之前，你应该先接入WIFI
    import heartbeat
    import machine
    if not heartbeat.check_online():
        heartbeat.try_login(USERNAME, PASSWD, SRUN_IP)
        
    # 进入5分钟的深度睡眠以节约用电
    machine.deepsleep(5*60*1000)
    machine.reset()
    ```