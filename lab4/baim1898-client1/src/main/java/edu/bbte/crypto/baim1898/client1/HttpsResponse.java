package edu.bbte.crypto.baim1898.client1;

public class HttpsResponse {
    private final String rawResponse, body;

    public HttpsResponse(String rawResponse) {
        this.rawResponse = rawResponse;
        body = bodyFromRawResponse(rawResponse);
    }

    private String bodyFromRawResponse(String rawResponse) {
        //find the first empty line (that signals the beginning of the body)
        int bodyStart = rawResponse.indexOf("\n\n");
        return rawResponse.substring(bodyStart).trim();
    }

    public String getRawResponse() {
        return rawResponse;
    }

    public String getBody() {
        return body;
    }
}
