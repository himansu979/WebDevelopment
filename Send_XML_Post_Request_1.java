
/*
https://www.chillyfacts.com/java-send-soap-xml-request-read-response/
https://www.youtube.com/watch?v=gmqjAennHbc

go to notepad ... paste xml ... ctrl+h .... 
replace " with \"

*/

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Send_XML_Post_Request_1 {
    public static void main(String[] args) {
        try {

            //String url = "http://www.holidaywebservice.com/HolidayService_v2/HolidayService2.asmx?op=GetHolidaysAvailable";

            String url = "http://www.dneonline.com/calculator.asmx?op=Add";
            URL obj = new URL(url);

            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            //con.setRequestProperty("Content-Type","application/soap+xml; charset=utf-8");

            con.setRequestProperty("Content-Type","text/xml; charset=utf-8");

            /*
            String countryCode="Canada";
            String xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>" +
            "<soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\"> " +
            " <soap12:Body> " +
            " <GetHolidaysAvailable xmlns=\"http://www.holidaywebservice.com/HolidayService_v2/\"> " +
            " <countryCode>"+countryCode+"</countryCode>" +
            " </GetHolidaysAvailable>" +
            " </soap12:Body>" +
            "</soap12:Envelope>";
            */

            String xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?> <soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"> <soap:Body> <Add xmlns=\"http://tempuri.org/\"> <intA>10</intA> <intB>5</intB> </Add> </soap:Body> </soap:Envelope>";
            System.out.println(url);
            System.out.println(xml);

            con.setDoOutput(true);

            DataOutputStream wr = new DataOutputStream(con.getOutputStream());
            wr.writeBytes(xml);
            wr.flush();
            wr.close();

            String responseStatus = con.getResponseMessage();
            System.out.println(responseStatus);

            BufferedReader in = new BufferedReader( new InputStreamReader(con.getInputStream()) );
            String inputLine;
            StringBuffer response = new StringBuffer();
            
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            in.close();

            System.out.println("response:" + response.toString());
        
        } catch (Exception e) {
            System.out.println(e);
        }

    } // main loop
} // class loop


