///类似 alert  单纯输出一段文字  使用方式:  Alert("hello world");
function Alert(message) {
    art.dialog({
        content: message
    });
}

//锁屏    使用方式   ShowLoading(); 或 ShowLoading("**********");
var LoadingDialog = null;
function ShowLoading(message) {
    if (LoadingDialog != null) {
        CloseLoading();
    }
    if (message == null || $.trim(message) == "") {
        message = 'hanling';
    }

    LoadingDialog = Art.dialog({
        lock: true,
        background: '#C4BDBD', // 背景色
        opacity: 0.87,	// 透明度
        content: message,
        ok: false,
        cancel: false
    });

}

//取消锁屏   使用方式： 当使用了ShowLoading() 锁屏后，  在使用 CloseLoading() 取消锁屏;
function CloseLoading() {
    if (LoadingDialog != null) {
        LoadingDialog.close();
        LoadingDialog = null;
    }
}



///类似 confirm()   message是提示语   okfun 是点击确定时的回调函数  cancelfun是点击取消时的回调函数
//使用方式    Confirm("是否取得删除？",function(){  },function(){  });   或者  Confirm("是否取得删除？",OkFun(), CancelFun());  
function Confirm(message, okfun, cancelfun) {
    var _confirm = art.dialog({
        id: 'testID',
        content: message,
        button: [
            {
                name: '确定',
                callback: function () {
                    if (okfun != null) {
                        okfun();
                    }
                },
                focus: true
            },
            {
                name: '取消',
                callback: function () {
                    if (cancelfun != null) {
                        cancelfun();
                    }
                    _confirm.close();
                    return false;
                }
            }
        ]
    });

}
