package self.skzeratal.tilelocalization;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import org.opencv.android.OpenCVLoader;

import self.skzeratal.tilelocalization.camera.CameraActivity;
import self.skzeratal.tilelocalization.floorplan.FloorPlanActivity;

public class MainActivity extends AppCompatActivity implements OnPostExecuted {
    static
    {
        if (OpenCVLoader.initDebug())
        {
            Log.d("MainActivity", "OpenCV was configured or connected successfully");
        }
        else
        {
            Log.d("MainActivity", "Sorry, OpenCV was BAW");
        }
    }
    Button testButton;
    Button localizationButton;
    Button floorPlanButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        testButton = findViewById(R.id.testButton);
        testButton.setOnClickListener(menuButtonOnClickListener);

        localizationButton = findViewById(R.id.localizationButton);
        localizationButton.setOnClickListener(menuButtonOnClickListener);

        floorPlanButton = findViewById(R.id.floorPlanButton);
        floorPlanButton.setOnClickListener(menuButtonOnClickListener);
    }

    Button.OnClickListener menuButtonOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View view) {
            Intent intent;

            switch (view.getId()) {
                case R.id.localizationButton:
                    intent = new Intent(MainActivity.this, CameraActivity.class);
                    intent.putExtra("Type", "Localization");
                    startActivityForResult(intent, 0);
                    break;
                case R.id.floorPlanButton:
                    intent = new Intent(MainActivity.this, FloorPlanActivity.class);
                    intent.putExtra("Type", "UpdateFeature");
                    startActivity(intent);
                    break;
                case R.id.testButton:
                    SocketClient socketClient = new SocketClient(MainActivity.this);
                    break;
            }
        }
    };

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == Activity.RESULT_OK) {
            int x = data.getIntExtra("X", -1);
            int y = data.getIntExtra("Y", -1);
            /*
            if (x != -1 && y != -1) {
                Intent intent = new Intent(MainActivity.this, FloorPlanActivity.class);
                intent.putExtra("Type", "MatchFeature");
                intent.putExtra("X", x);
                intent.putExtra("Y", y);
                startActivity(intent);
            }
            */
        }
    }

    @Override
    public void onPostExecuted(String result) {

    }
}