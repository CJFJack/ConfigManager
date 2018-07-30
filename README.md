# ConfigManager
##1. 首页

    展示登录用户欢迎语
##2. 发布管理

    ###2.1 配置管理

        ####2.1.1 配置修改

            列表字段：
                站点名称
                发布注意事项
                配置文件：配置文件名称、修改（点击后可进入该站点该配置文件的修改页面）、历史记录（点击后进入该站点该配置文件所有修改历史记录列表）   
                所属ECSi 配置状态 操作：站点所属ECS列表、配置生效状态，若状态为待生效，则待生效字体为红色，及后面出现发布按钮，点击后可生成xml格式的配置文件，存放路径为/release/<站点名称>/<服务器名称>/<配置文件名>.xml
                所属ECS SLB状态 健康状态 操作：与SLB列表页面类似，可以移除或添加站点关联的所有SLB的后端服务器状态
                健康检查：刷新站点关联SLB的后端服务器健康状态
                配置修改人
                配置修改时间
        ####2.1.2 待生效配置
        
            与配置修改相同，只显示待生效配置的站点列表
        ####2.1.3 配置文件内容修改页面

            点击配置修改页，对应站点配置文件的修改按钮
            只读字段：站点名、配置文件名、显示关联站点勾选框
            可编辑字段：修改站点（默认为全选所有关联站点，保存后同时修改勾选站点的同名配置文件）
            配置内容：textarea
        ####2.1.4 配置文件历史记录列表

            点击配置修改页，对应站点配置文件的历史记录按钮进入
            字段：
                修改编号、站点名称、配置文件名、修改人、修改时间、操作（恢复、查看内容）
        ####2.1.5 权限管理

            只有超级管理员组、运维工程师组、运维经理组中账号可看见此菜单            
    ###2.2 发布管理

        ####2.2.1 待发布申请

            状态为待发布的发布申请单列表
        ####2.2.2 发布申请列表

            所有发布申请单列表
            只有超级管理员组、运维工程师组、运维经理组中账号可看见删除按钮
        ####2.2.3 创建发布申请

            填写申请编号、期望发布日期、期望发布日期、期望发布日期、选择发布站点（可以添加多个）
        ####2.2.4 权限管理
     
           有相关权限人员可以进入
##3. 系统管理

    ###3.1 ECS管理

        ####3.1.1 ECS列表
   
            a. 字段：
                可通过阿里云接口更新，原则上不开放修改：区域、网络类型（经典、专用）、ECS名称、系统类型、系统版本、内网IP地址、外网IP地址、配置规格、运行状态、过期时间。修改人，修改日期、操作（修改、启用、禁用、删除、刷新监控数据、刷新基础信息）、CPU使用率、内存使用率、磁盘使用率
                    其中：CPU、内存。磁盘使用率若超过70%则显示红色字体
                不可更新、不可修改：实例ID（唯一标识）、使用状态
            b. 同步所有ECS
                通过阿里云SDK包调用阿里云API接口，获取所有ECS实例ID，本地没有则插入，本地有阿里云有则删除                
            c. 刷新所有ECS基础信息
                通过阿里云SDK包调用阿里云API接口，获取ECS信息的dict，通过与本地ECS的实例ID匹配，更新ECS基础信息
            d. 刷新所有ECS监控数据
                通过阿里云SDK包调用阿里云API接口，或者所有ECS的CPU、内存及磁盘使用率，并更新到数据库
            建议点击顺序：同步所有ECS--》刷新所有ECS基础信息--》刷新所有ECS监控数据
        ####3.1.2 ECS修改页面
  
            点击ECS列表页面--ECS名称超链接进入
    ###3.2 站点管理

        ####3.2.1 站点列表
       
            展示字段：站点名称、站点简称、配置文件夹名称、配置文件名称、所属ECS
            操作：修改、删除
        ####3.2.2 添加站点
      
            填写表单：站点名称、站点简称、配置文件夹名称、配置文件、所属ECS、所属站点族、端口号、测试页面、状态、研发负责人、发布注意事项
        ####3.2.3 修改站点
     
            点击站点列表--站点名称超链接进入
    ###3.3 SLB管理

        ####3.3.1 SLB列表
       
            a. 同步SLB基本信息
                通过阿里云SDK包调用阿里云API接口，获取所有SLB实例，本地没有则添加，本地有阿里云无则删除，本地有阿里云有则更新相关字段（实例别名、实例状态、实例IP、IP地址类型、创建时间）
                请求后需要添加遮盖层及loading样式，响应成功后关闭
            b. 刷新所有SLB健康信息
                通过阿里云SDK包调用阿里云API接口，刷新所有SLB后端服务器健康状态
                请求后需要添加遮盖层及loading样式，响应成功后关闭
            c. 其他字段：
                后端服务器健康状态（ECS名称 SLB状态 健康状态 操作）
                    SLB状态为已移除、健康状态非正常，字体颜色为红色
                    操作：
                        移除、添加SLB：通过阿里云SDK包调用阿里云API接口，添加或移除后端服务器，请求后需要添加遮盖层及loading样式，响应成功后关闭
                关联站点列表（站点列表）
            d. 点击实例ID超链接，可以进入添加关联站点页面
    ###3.4 权限管理

        只有超级管理员组、运维工程师组、运维经理组中账号可看见此菜单
##4. 退出

    退出登录，返回登录页面
##5. 登录界面

    引用django/admin登录界面
    views.py所有函数及类需要加login装饰器验证请求用户登录情况
##6. 账号管理

    使用django/admin功能管理

