

function Channel(channelId) {
    this.ws = undefined;  // web socket object
    this.channelId = channelId;
    this.decryptor = undefined;
    this.connector = undefined;

    // bind events
    var self = this;
    document.querySelector('#' + this.channelId + ' > .channel-connect-btn').onclick = function() {
        self.connector = document.querySelector('#' + self.channelId + ' > .channel-connector').value;
        self.decryptor = document.querySelector('#' + self.channelId + ' > .channel-decryptor').value;
        self.connect();
    };
};

Channel.prototype.connect = function() {
    if ('WebSocket' in window)  {
        this.ws = new WebSocket('ws://' + this.connector);
        var ws = this.ws;
        ws.onopen = function() {
            //ws.send('Message to send');
            console.log('Message is sent...');
        };
        ws.onmessage = function (evt) { 
            console.log('Message is received...');
            var data = evt.data;
            console.log('received : ' + data);
        };
        ws.onclose = function() { 
            console.log('Connection is closed...'); 
        };
    } else {
        console.log('WebSocket NOT supported by your Browser!');
    }

};


Channel.prototype.send = function(data) {
};

//<div id='sse'>
//  <a href='javascript:WebSocketTest()'>Run WebSocket</a>
//</div>

