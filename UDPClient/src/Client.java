import java.util.List;
import java.io.*;
import java.net.*;
import java.net.DatagramPacket;

public class Client {
	public String hostName;	
	public List<Server> servers;
		
	public Client(List<Server> s, String hN) {
		this.hostName = hN;
		this.servers = s;
	}
	
	public void sendChange(Server s) {
		byte[] sendData = 
		
		try {
			DatagramSocket ds = new DatagramSocket();					
		} catch (SocketException e) {		
			e.printStackTrace();
		} 
		
		try {
			InetAddress ipAddress = InetAddress.getByName(s.hostName);
			DatagramPacket sendPacket = new DatagramPacket(, Integer.SIZE, ipAddress, s.portNumber);
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
		
		
	}
	
	public void sendCommit() {
		
	}
	
	public void sendAbort() {
		
	}
	
	
}
