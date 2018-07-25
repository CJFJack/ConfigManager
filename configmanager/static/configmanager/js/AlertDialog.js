///���� alert  �������һ������  ʹ�÷�ʽ:  Alert("hello world");
function Alert(message) {
    art.dialog({
        content: message
    });
}

//����    ʹ�÷�ʽ   ShowLoading(); �� ShowLoading("**********");
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
        background: '#C4BDBD', // ����ɫ
        opacity: 0.87,	// ͸����
        content: message,
        ok: false,
        cancel: false
    });

}

//ȡ������   ʹ�÷�ʽ�� ��ʹ����ShowLoading() ������  ��ʹ�� CloseLoading() ȡ������;
function CloseLoading() {
    if (LoadingDialog != null) {
        LoadingDialog.close();
        LoadingDialog = null;
    }
}



///���� confirm()   message����ʾ��   okfun �ǵ��ȷ��ʱ�Ļص�����  cancelfun�ǵ��ȡ��ʱ�Ļص�����
//ʹ�÷�ʽ    Confirm("�Ƿ�ȡ��ɾ����",function(){  },function(){  });   ����  Confirm("�Ƿ�ȡ��ɾ����",OkFun(), CancelFun());  
function Confirm(message, okfun, cancelfun) {
    var _confirm = art.dialog({
        id: 'testID',
        content: message,
        button: [
            {
                name: 'ȷ��',
                callback: function () {
                    if (okfun != null) {
                        okfun();
                    }
                },
                focus: true
            },
            {
                name: 'ȡ��',
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
