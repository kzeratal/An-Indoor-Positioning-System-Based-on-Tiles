package self.skzeratal.tilelocalization;

import android.os.AsyncTask;
import android.util.Log;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

import self.skzeratal.tilelocalization.croppedimage.CroppedImageActivity;
import self.skzeratal.tilelocalization.floorplan.FloorPlanActivity;

public class SocketClient extends AsyncTask<String, Void, Void> {
    private OnPostExecuted object;
    private String type;
    private Socket socket;
    public String queue;

    public SocketClient () {
        socket = new Socket();
        queue = "";
    }

    public SocketClient (OnPostExecuted object) {
        this.object = object;
        socket = new Socket();
        queue = "";
    }

    @Override
    protected Void doInBackground(String... data) {
        type = data[0];

        switch (type) {
            case "STORE":
                store(data);
                break;
            case "UPDATE":
                break;
            case "RESTORE":
                restore();
                break;
            case "MATCH":
                match(data);
                break;
            case "MATC1":
                matc1(data);
                break;
            case "MATC2":
                matc2(data);
                break;
        }
        return null;
    }

    protected void onPostExecute(Void result) {
        switch (type) {
            case "STORE":
                object.onPostExecuted(queue);
                break;
            case "RESTORE":
                object.onPostExecuted(queue);
                break;
            case "MATCH":
                object.onPostExecuted(queue);
                break;
            case "MATC1":
                object.onPostExecuted(queue);
                break;
            case "MATC2":
                object.onPostExecuted(queue);
                break;
        }
    }

    public void Stop() {
        try {
            socket.close();
        }
        catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private void store(String... data) {
        try {
            String payloadSegment;
            socket = new Socket();
            socket.setSoTimeout(60000);
            socket.connect(new InetSocketAddress("140.123.97.87", 6666));
            socket.getOutputStream().write("STORE".getBytes());

            while (data[1].length() > 0) {
                if (data[1].length() >= 1024) {
                    payloadSegment = data[1].substring(0, 1024);
                    data[1] = data[1].substring(1024);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }
                else {
                    payloadSegment = data[1];
                    data[1] = data[1].substring(0, 0);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }
            }

            socket.getOutputStream().write((";" + data[2] + ";" + data[3] + ";" + data[4] + ";" + data[5] + ";STORE").getBytes());

            byte[] message = new byte[1024];
            int count = socket.getInputStream().read(message, 0, 1024);

            if (count > 0) {
                String payload = new String(message, "UTF-8");
                queue += payload.substring(5, count - 5);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private void restore() {
        byte[] message = new byte[1024];

        try {
            socket = new Socket();
            socket.setSoTimeout(5000);
            socket.connect(new InetSocketAddress("140.123.97.87", 6666));
            socket.getOutputStream().write("RESTORE".getBytes());

            int count = 0;

            do {
                 count = socket.getInputStream().read(message, 0, 1024);

                 if (count > 0) {
                     String payload = new String(message, "UTF-8");
                     queue += payload.substring(0, count);

                     if (queue.endsWith("RESTORE")) {
                         if (queue.startsWith("RESTORE")) {
                             queue = queue.substring(7, queue.length() - 7);
                         }
                         else {
                             queue = "";
                         }
                         break;
                     }
                 }
            } while (count > 0);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void test(String...data) {

    }

    private void match(String... data) {
        try {
            String payloadSegment;

            socket = new Socket();
            socket.setSoTimeout(60000);
            socket.connect(new InetSocketAddress("140.123.97.102", 6666));
            socket.getOutputStream().write("MATCH".getBytes());

            while (data[1].length() > 0) {
                if (data[1].length() >= 1024) {
                    payloadSegment = data[1].substring(0, 1024);
                    data[1] = data[1].substring(1024);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }
                else {
                    payloadSegment = data[1];
                    data[1] = data[1].substring(0, 0);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }

            }

            socket.getOutputStream().write((";" + data[2] + ";MATCH").getBytes());

            byte[] message = new byte[1024];
            int count = socket.getInputStream().read(message, 0, 1024);

            if (count > 0) {
                String payload = new String(message, "UTF-8");
                queue += payload.substring(5, count - 5);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private void matc1(String... data) {
        try {
            String payloadSegment;

            socket = new Socket();
            socket.setSoTimeout(60000);
            socket.connect(new InetSocketAddress("140.123.97.87", 6666));
            socket.getOutputStream().write("MATC1".getBytes());

            while (data[1].length() > 0) {
                if (data[1].length() >= 1024) {
                    payloadSegment = data[1].substring(0, 1024);
                    data[1] = data[1].substring(1024);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }
                else {
                    payloadSegment = data[1];
                    data[1] = data[1].substring(0, 0);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }
            }

            socket.getOutputStream().write((";" + data[2] + ";MATC1").getBytes());

            byte[] message = new byte[1024];
            int count = socket.getInputStream().read(message, 0, 1024);

            if (count > 0) {
                String payload = new String(message, "UTF-8");
                queue += payload.substring(5, count - 5);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private void matc2(String... data) {
        try {
            String payloadSegment;

            socket = new Socket();
            socket.setSoTimeout(60000);
            socket.connect(new InetSocketAddress("140.123.97.87", 6666));
            socket.getOutputStream().write("MATC2".getBytes());

            while (data[1].length() > 0) {
                if (data[1].length() >= 1024) {
                    payloadSegment = data[1].substring(0, 1024);
                    data[1] = data[1].substring(1024);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }
                else {
                    payloadSegment = data[1];
                    data[1] = data[1].substring(0, 0);
                    socket.getOutputStream().write(payloadSegment.getBytes());
                }

            }

            socket.getOutputStream().write((";" + data[2] + ";MATC2").getBytes());

            byte[] message = new byte[1024];
            int count = socket.getInputStream().read(message, 0, 1024);

            if (count > 0) {
                String payload = new String(message, "UTF-8");
                queue += payload.substring(5, count - 5);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}