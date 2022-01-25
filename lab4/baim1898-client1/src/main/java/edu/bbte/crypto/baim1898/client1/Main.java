package edu.bbte.crypto.baim1898.client1;

import sun.security.x509.GeneralName;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLPeerUnverifiedException;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.*;
import java.net.URL;
import java.net.UnknownHostException;
import java.security.cert.Certificate;
import java.security.cert.CertificateExpiredException;
import java.security.cert.CertificateParsingException;
import java.security.cert.X509Certificate;
import java.util.Collection;
import java.util.List;

public class Main {
    private static final String HOST = "www.bnr.ro";
    private static final int PORT = 443;

    public static void main(String[] args) {
        HttpsClient client = null;
        try {
            client = new HttpsClient(HOST, PORT);

            System.out.println("Secure connection established successfully.");
        } catch (Exception e) {
            System.out.println("Error while establishing connection: " + e.getMessage());
            return;
        }

        try {
            System.out.println("Sending GET request...");

            HttpsResponse response = client.get("/Home.aspx");

            System.out.println("Received response.");

            FileWriter fileWriter = new FileWriter("homepage.txt");
            fileWriter.write(response.getBody());
            fileWriter.close();

            System.out.println("Saved HTML to \"homepage.txt\".");
        } catch (IOException e) {
            System.out.println("Error getting homepage: " + e.getMessage());
            return;
        }

        try {
            Certificate[] certificates = client.getCertificates();

            System.out.println("\n\nCertificates retrieved: " + certificates.length);

            int index = 1;
            for (Certificate c : certificates) {
                System.out.println("***********************************************************************");

                if(c instanceof X509Certificate) {
                    X509Certificate x = (X509Certificate)c;
                    System.out.println("Certificate " + index + ":\n");

                    System.out.println("Version number: " + x.getVersion());
                    System.out.println("Serial number: " + x.getSerialNumber());
                    System.out.println("Issuer name: " + x.getIssuerX500Principal().getName());

                    System.out.println("Not before: " + x.getNotBefore());
                    System.out.println("Not after: " + x.getNotAfter());

                    System.out.println("Subject name: " + x.getSubjectX500Principal().getName());
                    System.out.println("Algorithm: " + x.getPublicKey().getAlgorithm());
                    System.out.println("Public key: " + x.getPublicKey());

                    System.out.println();

                    index++;
                }
            }
        } catch (SSLPeerUnverifiedException e) {
            e.printStackTrace();
        }
    }
}
