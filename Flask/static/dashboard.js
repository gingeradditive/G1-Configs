function appenNotification(message, level){
    $(".NotificationsArea").append('<div class="alert alert-'+level+' alert-dismissible fade show" role="alert">'+message+'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
}

$.ajax({
    url: '/tools/backend/check-files',
    method: 'GET',
    dataType: 'json',
    success: function (response) {
        if(response["KlipperScreen.conf"] == null){
            appenNotification("<strong>KlipperScreen.conf file not found</strong> this may cause G1 to malfunction, please restore the file via the utility menu","danger");
        }
        else if (response["KlipperScreen.conf"] == false){
            appenNotification("<strong>KlipperScreen.conf file has been modified or needs to be updated</strong>, please restore it via the utility menu","warning");
        }
        
        if(response["kamp.cfg"] == null){
            appenNotification("<strong>kamp.cfg file not found</strong> this may cause G1 to malfunction, please restore the file via the utility menu","danger");
        }
        else if (response["kamp.cfg"] == false){
            appenNotification("<strong>kamp.cfg file has been modified or needs to be updated</strong>, please restore it via the utility menu","warning");
        }

        if(response["moonraker.conf"] == null){
            appenNotification("<strong>moonraker.conf file not found</strong> this may cause G1 to malfunction, please restore the file via the utility menu","danger");
        }
        else if (response["moonraker.conf"] == false){
            appenNotification("<strong>moonraker.conf file has been modified or needs to be updated</strong>, please restore it via the utility menu","warning");
        }

        if(response["splash.png"] == null || response["theme/custom.css"] == null || response["theme/navi.json"] == null){
            appenNotification("<strong>Error some theme files seem to be missing</strong>, please restore the .theme folder via the uitlity menu","danger");
        }
        else if (response["splash.png"] == false || response["theme/custom.css"] == false || response["theme/navi.json"] == false){
            appenNotification("<strong>Warning some theme files seem to be corrupted</strong>, please restore the .theme folder via the uitlity menu","warning");
        }
    },
    error: function (xhr, status, error) {

    }
});