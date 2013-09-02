

function Channel(channelId) {
    this.ws = undefined;  // web socket object
    this.channelId = channelId;

    this.decryptorLabel = document.querySelector('#' + channelId + ' > .decryptor');
    this.connectorLabel = document.querySelector('#' + channelId + ' > .connector');
    this.statusLabel = document.querySelector('#' + channelId + ' > .status');
    this.connectButton = document.querySelector('#' + channelId + ' > .connect-btn');
    this.sendButton = document.querySelector('#' + channelId + ' > .send-btn');

    // bind events
    var self = this;

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
            self.connectorLabel.disabled = true;
            self.decryptorLabel.disabled = true;
            self.statusLabel.innerHTML= 'connected';
        };

        ws.onmessage = function (evt) { 
            var data = evt.data;
            console.log('received : ' + data);
        };

        ws.onclose = function() { 
            self.connectorLabel.disabled = false;
            self.decryptorLabel.disabled = false;
            self.statusLabel.innerHTML = 'closed';
        };
    } else {
        console.log('WebSocket NOT supported by your Browser!');
    }
};


Channel.prototype.send = function() {
};

//<div id='sse'>
//  <a href='javascript:WebSocketTest()'>Run WebSocket</a>
//</div>

