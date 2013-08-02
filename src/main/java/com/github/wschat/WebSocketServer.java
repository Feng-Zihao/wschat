
package com.github.wschat;

import java.io.IOException;
import java.net.ServerSocket;
import java.nio.ByteBuffer;

public class WebSocketServer implements Runnable {

	public final int port;
	ServerSocket serverSocket;

	public WebSocketServer(int port) throws IOException {
		this.port = port;
		serverSocket = new ServerSocket(port);
	}

	public void run() {
	}

	public static void main(String[] args) throws IOException {
		WebSocketServer server = new WebSocketServer(50000);
		server.run();
	}
}
