function openTerminal(options) {
    if (!$.isEmptyObject($('.terminal')[0])){
        alert("请先退出当前Terminal(CTRL+D或exit)")
        return
    }
    var client = new WSSHClient();

    var term = new Terminal({cols: 80, rows: 24, screenKeys: true, useStyle: true});
    term.on('data', function (data) {
        client.sendClientData(data);
    });
    term.open();
    $('.terminal').detach().appendTo('#term');
    $("#term").show();
    term.write('Connecting...' + '\r\n');

    client.connect({
        onError: function (error) {
            term.write('Error: ' + error + '\r\n');
            console.debug('Error: '+error);
            alert('Error: '+error)
            term.destroy();
        },
        onConnect: function () {
            client.sendInitData(options);
            // client.sendClientData('\r');
            console.debug('connection established');
        },
        onClose: function (e) {
            term.write("\rconnection closed")
            console.debug(e);
            //document.getElementById('term').style.display="none";
            term.destroy();
        },
        onData: function (data) {
            term.write(data);
            console.debug('get data:' + data);
        }
    })

}


var charWidth = 6.2;
var charHeight = 15.2;

/**
 * for full screen
 * @returns {{w: number, h: number}}
 */
function getTerminalSize() {
    var width = window.innerWidth;
    var height = window.innerHeight;
    return {
        w: Math.floor(width / charWidth),
        h: Math.floor(height / charHeight)
    };
}


function store(options) {
    window.localStorage.host = options.host
    window.localStorage.port = options.port
    window.localStorage.username = options.username
    window.localStorage.ispwd = options.ispwd;
    window.localStorage.secret = options.secret
}

function check() {
    return validResult["host"] && validResult["port"] && validResult["username"];
}

function connect(event) {
    // var remember = $("#remember").is(":checked")
    var $li=$(event.target);
    var $tr= $li.parents('tr');

    var options = {
        host:$.trim( $tr.find(".host").text()),
        port:$.trim($tr.find(".port").text()),
        username:$.trim( $tr.find(".username").text()),
        ispwd: $.trim($tr.find(".password").text()),
        secret: $.trim($tr.find(".secret").text()),
    }
    console.debug(options);
    // if (remember) {
    //     store(options)
    // }
    // if (check()) {
    //     openTerminal(options)
    // } else {
    //     for (var key in validResult) {
    //         if (!validResult[key]) {
    //             alert(errorMsg[key]);
    //             break;
    //         }
    //     }
    // }
    openTerminal(options)
}