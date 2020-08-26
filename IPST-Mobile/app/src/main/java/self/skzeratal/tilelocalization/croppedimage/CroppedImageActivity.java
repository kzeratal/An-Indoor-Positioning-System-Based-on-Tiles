package self.skzeratal.tilelocalization.croppedimage;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfDouble;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.utils.Converters;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

import self.skzeratal.tilelocalization.BuildConfig;
import self.skzeratal.tilelocalization.OnPostExecuted;
import self.skzeratal.tilelocalization.R;
import self.skzeratal.tilelocalization.SocketClient;

public class CroppedImageActivity extends Activity implements OnPostExecuted {
    private TextView textView;
    private EditText editTextX;
    private EditText editTextY;
    private Button uploadButton;
    private String type;
    private float angleOfCamera;
    private float orientation;
    private float var;
    private boolean canQuit;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_croppedimage);
        if (angleOfCamera < 45/* || var < 100*/)
        {
            canQuit = true;
        }
        else
        {
            canQuit = false;
        }
        Uri originalImageUri = Uri.parse(Environment.getExternalStorageDirectory().getAbsolutePath() + "/Pictures/OriginalImage.png");
        Uri croppedImageUri = Uri.parse(Environment.getExternalStorageDirectory().getAbsolutePath() + "/Pictures/CroppedImage.png");
        Uri AdjustedImageUri = Uri.parse(Environment.getExternalStorageDirectory().getAbsolutePath() + "/Pictures/AdjustedImage.png");

        orientation = getIntent().getFloatExtra("o", 0f) - 125 + 45;
        angleOfCamera = getIntent().getFloatExtra("a", 0f);
        cropAndAdjustImage(originalImageUri, croppedImageUri, AdjustedImageUri, orientation);

        editTextX = findViewById(R.id.editTextX);
        editTextY = findViewById(R.id.editTextY);
        ImageView imageView = findViewById(R.id.imageView);
        imageView.setImageURI(croppedImageUri);
        Button returnButton = findViewById(R.id.returnButton);
        returnButton.setOnClickListener(returnButtonOnClickListener);
        uploadButton = findViewById(R.id.uploadButton);
        uploadButton.setOnClickListener(uploadButtonOnClickListener);
        Button buttonXPlus = findViewById(R.id.buttonXPlus);
        buttonXPlus.setOnClickListener(buttonXPlusOnClickListener);
        Button buttonYPlus = findViewById(R.id.buttonYPlus);
        buttonYPlus.setOnClickListener(buttonYPlusOnClickListener);
        Button buttonXMinus = findViewById(R.id.buttonXMinus);
        buttonXMinus.setOnClickListener(buttonXMinusOnClickListener);
        Button buttonYMinus = findViewById(R.id.buttonYMinus);
        buttonYMinus.setOnClickListener(buttonYMinusOnClickListener);
        textView = findViewById(R.id.textView);
        TextView textViewX = findViewById(R.id.textViewX);
        TextView textViewY = findViewById(R.id.textViewY);
        type = getIntent().getStringExtra("Type");
        String lastNameX = getIntent().getStringExtra("LastNameX");
        String lastNameY = getIntent().getStringExtra("LastNameY");
        textView.setText("");
        textView.setTextColor(Color.BLACK);
        switch (type) {
            case "Localization":
                buttonXPlus.setVisibility(View.INVISIBLE);
                buttonYPlus.setVisibility(View.INVISIBLE);
                buttonXMinus.setVisibility(View.INVISIBLE);
                buttonYMinus.setVisibility(View.INVISIBLE);
                editTextX.setVisibility(View.INVISIBLE);
                editTextY.setVisibility(View.INVISIBLE);
                textViewX.setVisibility(View.INVISIBLE);
                textViewY.setVisibility(View.INVISIBLE);
                break;
            case "UpdateFeature":
                buttonXPlus.setVisibility(View.VISIBLE);
                buttonYPlus.setVisibility(View.VISIBLE);
                buttonXMinus.setVisibility(View.VISIBLE);
                buttonYMinus.setVisibility(View.VISIBLE);
                editTextX.setVisibility(View.VISIBLE);
                editTextY.setVisibility(View.VISIBLE);
                textViewX.setVisibility(View.VISIBLE);
                textViewY.setVisibility(View.VISIBLE);
                editTextX.setText(lastNameX);
                editTextY.setText(lastNameY);
                break;
        }
    }

    Button.OnClickListener returnButtonOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View view) {
            finish();
        }
    };

    Button.OnClickListener uploadButtonOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View view) {
            textView.setText("");
            textView.setTextColor(Color.BLACK);
            uploadButton.setEnabled(false);
            File croppedImage = new File(Environment.getExternalStorageDirectory().getAbsolutePath() + "/Pictures/CroppedImage.png");
            File adjustedImage = new File(Environment.getExternalStorageDirectory().getAbsolutePath() + "/Pictures/AdjustedImage.png");

            int croppedImageSize = (int) croppedImage.length();
            int adjustedImageSize = (int) adjustedImage.length();
            byte[] croppedImageBytes = new byte[croppedImageSize];
            byte[] adjustedImageBytes = new byte[adjustedImageSize];
            try {
                BufferedInputStream croppedImageBuffer = new BufferedInputStream(new FileInputStream(croppedImage));
                BufferedInputStream adjustedImageBuffer = new BufferedInputStream(new FileInputStream(adjustedImage));
                croppedImageBuffer.read(croppedImageBytes, 0, croppedImageBytes.length);
                croppedImageBuffer.close();
                adjustedImageBuffer.read(adjustedImageBytes, 0, adjustedImageBytes.length);
                adjustedImageBuffer.close();
            } catch (FileNotFoundException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            //byte[] croppedImageBytes = Files.readAllBytes(croppedImage.getAbsolutePath());
            //byte[] adjustedImageBytes = Files.readAllBytes(adjustedImage.getAbsolutePath());
            String croppedImagePayload = Base64.encodeToString(croppedImageBytes, Base64.DEFAULT);
            String adjustedImagePayload = Base64.encodeToString(adjustedImageBytes, Base64.DEFAULT);

            SocketClient socketClient1 = new SocketClient(CroppedImageActivity.this);
            SocketClient socketClient2 = new SocketClient(CroppedImageActivity.this);

            switch (type) {
                case "Localization":
                    socketClient1.execute("MATC1", croppedImagePayload, String.valueOf(angleOfCamera));
                    if (angleOfCamera >= 60/* && var >= 100*/)
                    {
                        socketClient2.execute("MATC2", adjustedImagePayload, String.valueOf(angleOfCamera));
                    }
                    socketClient1.Stop();
                    socketClient2.Stop();
                    break;
                case "UpdateFeature":
                    String name = "X" + editTextX.getText().toString() + "Y" + editTextY.getText().toString();
                    String x = String.valueOf(getIntent().getFloatExtra("x", 0f));
                    String y = String.valueOf(getIntent().getFloatExtra("y", 0f));

                    socketClient1.execute("STORE", adjustedImagePayload, name, x, y, String.valueOf(angleOfCamera));
                    socketClient2.Stop();
                    break;
            }
        }
    };

    Button.OnClickListener buttonXPlusOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View view) {
            String currentX = editTextX.getText().toString();
            editTextX.setText(String.valueOf(Integer.parseInt(currentX) + 1));
        }
    };

    Button.OnClickListener buttonYPlusOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View view) {
            String currentY = editTextY.getText().toString();
            editTextY.setText(String.valueOf(Integer.parseInt(currentY) + 1));
        }
    };

    Button.OnClickListener buttonXMinusOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View view) {
            String currentX = editTextX.getText().toString();
            editTextX.setText(String.valueOf(Integer.parseInt(currentX) - 1));
        }
    };

    Button.OnClickListener buttonYMinusOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View view) {
            String currentY = editTextY.getText().toString();
            editTextY.setText(String.valueOf(Integer.parseInt(currentY) - 1));
        }
    };

    public void onPostExecuted(String result) {
        switch (type) {
            case "Localization":
                if (result.equals("BLURRY")) {
                    textView.setText("The Image is too Blurry");
                    textView.setTextColor(Color.RED);
                    uploadButton.setEnabled(true);
                }
                else if (result.equals("DAMAGED1")) {
                    textView.setText("連線不穩定1");
                    textView.setTextColor(Color.RED);
                    uploadButton.setEnabled(true);
                }
                else if (result.equals("DAMAGED2")) {
                    textView.setText("連線不穩定2");
                    textView.setTextColor(Color.RED);
                    uploadButton.setEnabled(true);
                }
                else {
                    textView.setText("MATC1 成功");
                    if (canQuit)
                    {
                        try
                        {
                            String name = result.substring(0, result.indexOf(","));
                            result = result.substring(result.indexOf(",") + 1);
                            int x = Math.round(Float.parseFloat(result.substring(0, result.indexOf(","))));
                            int y = Math.round(Float.parseFloat(result.substring(result.indexOf(",") + 1, result.indexOf(";"))));

                            Intent intent = new Intent();

                            intent.putExtra("Name", name);
                            intent.putExtra("X", x);
                            intent.putExtra("Y", y);
                            setResult(Activity.RESULT_OK, intent);
                            finish();
                        }
                        catch (StringIndexOutOfBoundsException ex)
                        {
                            textView.setText("連線不穩定3");
                            textView.setTextColor(Color.RED);
                            uploadButton.setEnabled(true);
                        }
                    }
                    else
                    {
                        canQuit = true;
                    }
                }
                break;
            case "UpdateFeature":
                if (result.equals("NAMEEXISTED")) {
                    textView.setText("The Name Already Exist");
                    textView.setTextColor(Color.RED);
                }
                else if (result.equals("BLURRY")) {
                    textView.setText("The Image is too Blurry");
                    textView.setTextColor(Color.RED);
                }
                else if (result.equals("DAMAGED1")) {
                    textView.setText("連線不穩定");
                    textView.setTextColor(Color.RED);
                }
                else if (result.equals("DAMAGED2")) {
                    textView.setText("連線不穩定");
                    textView.setTextColor(Color.RED);
                }
                else if (result.equals("SUCCESS")) {
                    Intent intent = new Intent();
                    intent.putExtra("NameX", editTextX.getText().toString());
                    intent.putExtra("NameY", editTextY.getText().toString());
                    setResult(100, intent);
                    finish();
                }
                break;
        }
    }

    private void cropAndAdjustImage(Uri originalImageUri, Uri croppedImageUri, Uri AdjustedImageUri, float orientation)
    {
        Mat originalImage = Imgcodecs.imread(originalImageUri.toString());
        int middleX = (int) originalImage.width() / 2;
        int middleY = (int) originalImage.height() / 2;
        int length;
        if (originalImage.width() > originalImage.height())
        {
            length = (int) (originalImage.height() * 0.25);
        }
        else
        {
            length = (int) (originalImage.width() * 0.25);
        }
        Rect rect = new Rect(middleX - length, middleY - length, length * 2, length * 2);
        Mat croppedImage = new Mat(originalImage, rect);
        Imgcodecs.imwrite(croppedImageUri.toString(), croppedImage);
        Mat adjustedImage = new Mat(length * 2, length * 2, CvType.CV_8UC4);

        List<Point> destination = new ArrayList<>();
        destination.add(new org.opencv.core.Point(0, length * 2));
        destination.add(new org.opencv.core.Point(0, 0));
        destination.add(new org.opencv.core.Point(length * 2, 0));
        destination.add(new org.opencv.core.Point(length * 2, length * 2));
        Mat destinationMat = Converters.vector_Point2f_to_Mat(destination);

        int radius = (int) Math.round(Math.pow(2, 0.5) * length);
        List<Point> source = new ArrayList<>();
        source.add(new org.opencv.core.Point(middleX + radius * Math.cos(Math.toRadians((180 - orientation) % 360)),middleY + radius * Math.sin(Math.toRadians((180 - orientation) % 360))));
        source.add(new org.opencv.core.Point(middleX + radius * Math.cos(Math.toRadians((270 - orientation) % 360)),middleY + radius * Math.sin(Math.toRadians((270 - orientation) % 360))));
        source.add(new org.opencv.core.Point(middleX + radius * Math.cos(Math.toRadians((-orientation) % 360)),middleY + radius * Math.sin(Math.toRadians((-orientation ) % 360))));
        source.add(new org.opencv.core.Point(middleX + radius * Math.cos(Math.toRadians((90 - orientation) % 360)),middleY + radius * Math.sin(Math.toRadians((90 - orientation) % 360))));
        Mat sourceMat = Converters.vector_Point2f_to_Mat(source);

        Mat perspectiveTransform = Imgproc.getPerspectiveTransform(sourceMat, destinationMat);
        Imgproc.warpPerspective(originalImage, adjustedImage, perspectiveTransform, new org.opencv.core.Size(length * 2, length * 2), Imgproc.INTER_CUBIC);
        Imgcodecs.imwrite(AdjustedImageUri.toString(), adjustedImage);

        Mat laplacianDestinationMat = new Mat();
        Mat laplacianGrayMat = new Mat();

        Imgproc.cvtColor(croppedImage, laplacianGrayMat, Imgproc.COLOR_BGR2GRAY);
        Imgproc.Laplacian(laplacianGrayMat, laplacianDestinationMat, 3);
        MatOfDouble median = new MatOfDouble();
        MatOfDouble standard = new MatOfDouble();
        Core.meanStdDev(laplacianDestinationMat, median , standard);

        var = (float) Math.pow(standard.get(0,0)[0],2);
    }
}