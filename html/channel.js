

function Channel(channelId) {
    this.ws = undefined;  // web socket object
    this.channelId = channelId;

    this.decryptorLabel = document.querySelector('#' + channelId + ' .decryptor');
    this.connectorLabel = document.querySelector('#' + channelId + ' .connector');
    this.statusLabel = document.querySelector('#' + channelId + ' .status');
    this.msgsDiv = document.querySelector('#' + channelId + ' .msgs');
    this.connectButton = document.querySelector('#' + channelId + ' .connect-btn');
    this.sendButton = document.querySelector('#' + channelId + ' .send-btn');
    this.msgInput = document.querySelector('#' + channelId + ' .msg-input');

    // bind events
    var self = this;
    //this.sendButton.disabled = true;

    // connect action
    this.connectButton.onclick = function() {
        self.connect();
    };

    this.sendButton.onclick = function() {
        self.send();
    }
};

Channel.prototype.connect = function() {
    if (this.ws !== undefined) {
        this.ws.close();
    }

    if ('WebSocket' in window)  {
        this.ws = new WebSocket('ws://' + this.connectorLabel.value);
        var self = this;
        var ws = this.ws;

        ws.onopen = function() {
            //self.connectorLabel.disabled = true;
            //self.decryptorLabel.disabled = true;
            //self.connectButton.disabled = true;
            //self.sendButton.disabled = false;
            self.statusLabel.innerHTML = 'connected';
            self.msgsDiv.innerHTML = '';
        };

        ws.onmessage = function (evt) { 
            var data = JSON.parse(evt.data);
            var date = new Date(data.time);
            self.msgsDiv.appendChild(document.createTextNode(date));
            self.msgsDiv.appendChild(document.createElement('br'));
            self.msgsDiv.appendChild(document.createTextNode(data.user));
            self.msgsDiv.appendChild(document.createElement('br'));
            self.msgsDiv.appendChild(document.createTextNode(data.text));
            self.msgsDiv.appendChild(document.createElement('br'));
            self.msgsDiv.appendChild(document.createElement('br'));
        };

        ws.onclose = function() { 
            //self.connectorLabel.disabled = false;
            //self.decryptorLabel.disabled = false;
            //self.connectButton.disabled = false;
            //self.sendButton.disabled = true;
            self.statusLabel.innerHTML = 'closed';
        };
    } else {
        console.log('WebSocket NOT supported by your Browser!');
    }
};


Channel.prototype.send = function() {
    console.log(this.msgInput.value);
    this.ws.send(this.msgInput.value);
    this.msgInput.value = '';
};

