package edu.bbte.crypto.baim1898.client1;

import javax.net.ssl.SSLPeerUnverifiedException;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.*;
import java.security.cert.Certificate;

public class HttpsClient {
    SSLSocket socket;
    PrintWriter out;
    BufferedReader in;

    /***
     * Create a HTTPS client and connects it to the specified host and port.
     * @param host The host to connect to.
     * @param port The port.
     */
    public HttpsClient(String host, int port) throws IOException {
        socket = (SSLSocket) SSLSocketFactory.getDefault().createSocket(host, port);
        socket.startHandshake();
    }

    public HttpsResponse get(String path) throws IOException {
        writeGet(path);
        return new HttpsResponse(readResponse());
    }

    private void writeGet(String path) throws IOException {
        if (out == null) {
            out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())));
        }

        System.out.println(socket.getApplicationProtocol());

        out.println("GET " + path + " HTTP/1.0");
        out.println();
        out.flush();
    }

    private String readResponse() throws IOException {
        if (in == null) {
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        }

        String inputLine;
        StringBuilder responseBuilder = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            responseBuilder.append(inputLine).append('\n');
        }

        return responseBuilder.toString();
    }

    public Certificate[] getCertificates() throws SSLPeerUnverifiedException {
        return socket.getSession().getPeerCertificates();
    }
}
