import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;

public class Client {
	public String hostName;	
	public List<Server> servers;
	DatagramSocket clientSocket;
		
	public Client(List<Server> s, String hN) {
		this.hostName = hN;
		this.servers = s;
	}
	
	public void sendChange(Server s) throws IOException {		
		clientSocket = new DatagramSocket();
		InetAddress ipAddress = InetAddress.getByName("localhost");
		byte[] sendData = ByteBuffer.allocate(4).putInt(Messages.CHANGE).array();
		byte[] receivedData = ByteBuffer.allocate(4).array();
						
		DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, ipAddress, s.portNumber);
		clientSocket.send(sendPacket);
		clientSocket.close();		
	}
	
	public void sendCommit() {
		
	}
	
	public void sendAbort() {
		
	}
	
	public static void main(String... args) throws IOException
	{
		List<Server> serverList = new ArrayList<Server>();	
		Server server = new Server("server01", 8888);
		
		serverList.add(server);
		Client client = new Client(serverList, "client01");
		
		client.sendChange(client.servers.get(0));
	}
}
