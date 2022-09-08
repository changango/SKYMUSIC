let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function updateUserList() {
    $.getJSON('api/v1/friend/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            if (currentUser === data[i]['friend_user1']['username'] || currentUser === data[i]['friend_user2']['username']){
                if(currentUser === data[i]['friend_user1']['username']){
                    if(data[i]['friend_user2']['is_status'] === 'online'){
                        const userItem =
                        `<a class="list-group-item user" style="display:block;" target="${data[i]['friend_user2']['username']}">
                            <span class="text-left">
                                ${data[i]['friend_user2']['nickname']}
                            </span>
                            <span class="text-right" style="color:green;float:right;">
                                在线
                            </span>
                        </a>`;
                        $(userItem).appendTo('#user-list');
                    }else if(data[i]['friend_user2']['is_status'] === 'offline'){
                        const userItem =
                        `<a class="list-group-item user" target="${data[i]['friend_user2']['username']}">
                            <span class="text-left">
                                ${data[i]['friend_user2']['nickname']}
                            </span>
                            <span class="text-right" style="color:grey;float:right;">
                                离线
                            </span>
                        </a>`;
                        $(userItem).appendTo('#user-list');
                    }
                }
                else if(currentUser === data[i]['friend_user2']['username']){
                    if(data[i]['friend_user1']['is_status'] === 'online'){
                        const userItem =
                        `<a class="list-group-item user" style="display:block;" target="${data[i]['friend_user1']['username']}">
                            <span class="text-left">
                                ${data[i]['friend_user1']['nickname']}
                            </span>
                            <span class="text-right" style="color:green;float:right;">
                                在线
                            </span>
                        </a>`;
                        $(userItem).appendTo('#user-list');
                    }else if(data[i]['friend_user1']['is_status'] === 'offline'){
                        const userItem =
                        `<a class="list-group-item user" target="${data[i]['friend_user1']['username']}">
                            <span class="text-left">
                                ${data[i]['friend_user1']['nickname']}
                            </span>
                            <span class="text-right" style="color:grey;float:right;">
                                离线
                            </span>
                        </a>`;
                        $(userItem).appendTo('#user-list');
                    }
                }
            };

        }
        $('.user').click(function () {
            let selected = event.target;
            setCurrentRecipient(selected.target);
        });
    });
}

// 刷新用户列表的用户状态
function showLogin()
{
	updateUserList();

}
setInterval("showLogin()","1000");

function drawMessage(message) {
    $.getJSON(`api/v1/user/?target=${message.user}`, function (data) {
        if (message.user === currentUser) {
            const messageItem = `
                <li class="message right">
                    <div class="row">
                        <div class="col-md-2"></div>
                        <div class="col-md-9 col-md-offset -1">
                            <div class="row">
                                <div class="col-md-9"><p class="text-right">${message.timestamp}</p></div>
                                <div class="col-md-3"><p class="text-center">${data[0]['nickname']}</p></div>
                            </div>
                            <div class="row">
                                <div class="text_wrapper">
                                    <div class="text">${message.body}
                                </div>
                            </div></div>
                        </div>
                        <div class="col-md-1" >
                            <img src="${data[0]['headprotrait']}" style="float: right;" class="img-circle" width="60" height="60">
                        </div>
                    </div>
                </li>`;
            $("#messages").append(messageItem);
        }
        else{
            const messageItem = `
            <li class="message left">
                <div class="row">
                    <div class="col-md-1">
                        <img src="${data[0]['headprotrait']}" class="img-circle" width="60" height="60">
                    </div>
                    <div class="col-md-9">
                        <div class="row">
                            <div class="col-md-3"><p class="text-center">${data[0]['nickname']}</p></div>
                            <div class="col-md-9"><p class="text-left">${message.timestamp}</p></div>
                        </div>
                        <div class="row">
                            <div class="text_wrapper">
                                <div class="text">${message.body}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </li>`;
            $("#messages").append(messageItem);
        };
    });
}

function getConversation(recipient) {

    $.getJSON(`api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    console.log(id)
    $.getJSON(`api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post('api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('发送失败！');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    updateUserList();
    disableInput();
    var socket = new WebSocket('ws://' + window.location.host +'/ws/chat/' + sessionKey +'/');
    console.log(123)
    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});



