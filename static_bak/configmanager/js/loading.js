 
var _PageHeight = document.documentElement.clientHeight,
    _PageWidth = document.documentElement.clientWidth;

var _LoadingTop = _PageHeight > 90 ? (_PageHeight - 90) / 2 : 0,
    _LoadingLeft = _PageWidth > 90 ? (_PageWidth - 90) / 2 : 0;

var _LoadingHtml = '<div id="loadingDiv" style="position:absolute;left:0;width:100%;height:' + _PageHeight + 'px;top:0;background:#FFFFFF;opacity:1.0;
                    filter:alpha(opacity=80);z-index:10000;">
                    <div class="spinner" style="position: top: 60px; margin:' + _LoadingTop + 'px auto ;"></div></div>';

document.write(_LoadingHtml);


document.onreadystatechange = completeLoading;


function completeLoading() {
    if (document.readyState == "complete") {
        
        $("#loadingDiv").fadeOut(1500);
    }
}
