# WeChatHelper

- 利用automation的方式模拟手工操作，实现预定的功能。

- 运行前需要先启动进入 WeChat,　启动后mouse/keyboard将用于模拟操作，不再可以人工干预，否则会造成执行错误，使程序中断

- 程序依赖界面，如果有的界面由于版本更新改动，程序需要随着修改

- 本程序基于Windows版本的WeChat开发调试

启动：

- 切换到项目所在的目录

    > cd WeChatHelper
    
- 根据settings目录下已有的设置文件调整修改设置内容，再执行：

    > python .\src\wechat_helper.py settins\xxxxxxx.yaml
