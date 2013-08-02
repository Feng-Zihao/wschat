package com.github.wschat.websocket;

import java.io.IOException;
import java.net.Socket;

public class WebSocket {
	public final Socket socket;

	public WebSocket(Socket socket) {
		this.socket = socket;
	}

	public DataFrame getInputDataFrame() throws IOException {
		return DataFrame.valueOf(socket.getInputStream());
	}

}
